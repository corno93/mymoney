from functools import lru_cache
from typing import Optional

import pandas as pd
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


def handle_save(data):
    """Save the file's contents to the data/data.csv"""

    # write all contents to file
    f1 = open(DATA_FILE, "a+")
    f1.write(data.decode("utf-8"))
    f1.close()


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
    df = df.loc[f"{year}-{month}-01":f"{year}-{month + 1}-01"]

    if not df.empty:

        # make another column that concatenates description and amount
        df["acc"] = df["description"] + ACC_COL_DELIMITER + df["amount"].astype(str)

        # group all data by day
        data_groupby_day = df.resample("D")

        # get each day's sum and add another column for normalized amount (for cell colouring)
        daily_amount_sum = data_groupby_day.amount.sum()
        normalized_daily_amount_sum = daily_amount_sum.apply(
            lambda x: -(x / daily_amount_sum.min())
            if x < 0
            else x / daily_amount_sum.max()
        )

        # for each day, join all of the new columns data
        daily_transactions = data_groupby_day.acc.agg(
            lambda x: DAILY_TRANSACTIONS_DELIMITER.join(x)
        )

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

    data = await file.read()
    handle_save(data)

    get_data.cache_clear()

    # sample the data to get a month and year
    _, month, year = data.decode("utf-8")[:15].split(",")[0].split("/")

    # remove trailing '0' (not great but it'll do)
    if "0" in month and month != "10":
        month = month[1:]

    return RedirectResponse(
        url=f"/calendar/year/{year}/month/{month}", status_code=HTTP_302_FOUND
    )
