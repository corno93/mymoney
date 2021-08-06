from io import StringIO

import pandas as pd
from fastapi import APIRouter, File, Request, UploadFile
from fastapi.responses import HTMLResponse

from spend_calendar import SpendCalendar
from templates import templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/upload", response_class=HTMLResponse)
async def upload(request: Request, file: UploadFile = File(...)):

    # save file to dir, validate
    data = await file.read()
    df = pd.read_csv(
        StringIO(data.decode("utf-8")),
        header=None,
        delimiter=",",
        usecols=[0, 1, 2],
        names=["date", "amount", "description"],
        parse_dates=["date"],
        dayfirst=True,
    )

    # pd
    daily_amount_sum = df.resample("D", on="date").amount.sum()
    cal = SpendCalendar(daily_amount_sum, 7, 2021)

    # pick first month year
    # first_year_month = (2021, 7)
    html_calendar = cal.formatmonth(2021, 7)

    return templates.TemplateResponse(
        "index.html", {"request": request, "calendar": html_calendar}
    )
