from datetime import datetime
from functools import lru_cache
from typing import Optional

import aiofiles
import pandas as pd
from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, File, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.status import HTTP_302_FOUND

from constants import ACC_COL_DELIMITER, DAILY_TRANSACTIONS_DELIMITER, DATA_FILE
from spend_calendar import SpendCalendar
from templates import templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


async def save_data(data):
    async with aiofiles.open(DATA_FILE, "a") as f:
        await f.write(data.decode("utf-8"))


@lru_cache()
def get_data():
    return pd.read_csv(
        DATA_FILE,
        header=None,
        delimiter=",",
        usecols=[0, 1, 2],
        names=["date", "amount", "description"],
        parse_dates=["date"],
        dayfirst=True,
        index_col="date",
    )


@router.get("/calendar/year/{year}/month/{month}", response_class=HTMLResponse)
async def calendar(request: Request, year: int, month: int):

    df = get_data()

    # FIXME: FutureWarning: Value based partial slicing on non-monotonic DatetimeIndexes
    #  with non-existing keys is deprecated and will raise a KeyError in a future Version.
    df = df.loc[
        f"{year}-{month}-01" : (
            datetime(year=year, month=month, day=1) + relativedelta(months=1)
        ).strftime("%Y-%m-%d")
    ]

    if not df.empty:

        # make another column that concatenates description and amount - this makes it easier
        # to display a list of transactions and each amount after grouping by day
        df["acc"] = df["description"] + ACC_COL_DELIMITER + df["amount"].astype(str)

        # group all data by day
        data_groupby_day = df.resample("D")

        # get each day's sum
        daily_amount_sum = data_groupby_day.amount.sum()

        # add another column for normalized amount - for cell colouring
        normalized_daily_amount_sum = daily_amount_sum.apply(
            lambda x: -(x / daily_amount_sum.min())
            if x < 0
            else x / daily_amount_sum.max()
        )

        # for each day, concatenate all of the 'acc' columns data for each day
        daily_transactions = data_groupby_day.acc.agg(
            lambda x: DAILY_TRANSACTIONS_DELIMITER.join(x)
        )

        # concatenate all series into a single dataframe
        df = pd.concat(
            [daily_amount_sum, daily_transactions, normalized_daily_amount_sum], axis=1
        )
        df.columns = ["amount", "transactions", "normalized_amount"]

    calendar = SpendCalendar(df, year, month)
    html_calendar = calendar.formatmonth()

    return templates.TemplateResponse(
        "index.html", {"request": request, "calendar": html_calendar}
    )


@router.post("/upload", response_class=RedirectResponse)
async def upload(
    request: Request, file: UploadFile = File(...), redirect: Optional[str] = None
):
    # always save the data and invalidate cache
    data = await file.read()
    await save_data(data)
    get_data.cache_clear()

    # if theres no redirect url, sample a bit of the data to get the first month and year
    if not redirect:
        _, month, year = data.decode("utf-8")[:15].split(",")[0].split("/")

        # remove trailing '0'
        if "0" in month and month != "10":
            month = month[1:]

        redirect = f"/calendar/year/{year}/month/{month}"

    return RedirectResponse(url=redirect, status_code=HTTP_302_FOUND)
