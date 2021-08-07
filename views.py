import pandas as pd
from fastapi import APIRouter, File, Request, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.status import HTTP_302_FOUND

from constants import DATA_FILE
from spend_calendar import SpendCalendar
from templates import templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


async def handle_save(data):
    """Save the file's contents to the data/data.csv"""

    # write all contents to file
    f1 = open(DATA_FILE, "a+")
    f1.write(data.decode("utf-8"))
    f1.close()


@router.get("/calendar/year/{year}/month/{month}", response_class=HTMLResponse)
async def calendar(request: Request, year: int, month: int):
    df = pd.read_csv(
        DATA_FILE,
        header=None,
        delimiter=",",
        usecols=[0, 1, 2],
        names=["date", "amount", "description"],
        parse_dates=["date"],
        dayfirst=True,
    )
    daily_amount_sum = df.resample("D", on="date").amount.sum()
    cal = SpendCalendar(daily_amount_sum, year, month)
    html_calendar = cal.formatmonth(year, month)

    return templates.TemplateResponse(
        "index.html", {"request": request, "calendar": html_calendar}
    )


@router.post("/upload", response_class=RedirectResponse)
async def upload(request: Request, file: UploadFile = File(...)):

    data = await file.read()
    await handle_save(data)

    # sample the data to get a month and year
    _, month, year = data.decode("utf-8")[:20].split(",")[0].split("/")
    # remove trailing '0' (not great but it'll do)
    if "0" in month and month != "10":
        month = month[1:]
    return RedirectResponse(
        url=f"/calendar/year/{year}/month/{month}", status_code=HTTP_302_FOUND
    )
