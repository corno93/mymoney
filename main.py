
import os
import pandas as pd
from calendar import HTMLCalendar

"""
Stupid script to read combank csv and output monthly spend

cols:
date, amount, description, acc total (smart access)

"""

class MyCalendar(HTMLCalendar):

    def __init__(self, daily_amount_sum, month, year, *args, **kwargs):
        self.daily_amount_sum = daily_amount_sum
        self.month = month
        self.year = year
        super().__init__(*args, **kwargs)

    def formatday(self, day, weekday):

        day_html = super(MyCalendar, self).formatday(day, weekday)

        if day != 0:

            try:
                daily_amount = self.daily_amount_sum[f"{self.year}-{self.month}-{day}"]
            except KeyError as e:
                daily_amount = 0

            # inject new data
            div_class = "green" if daily_amount > 0 else "red"
            amount_div = f'<div class="{div_class}">{str(daily_amount)}</div>'
            day_html = f"{day_html[:-5]}{amount_div}</td>"

        return day_html




file_path = os.path.abspath("01_01_2021_to_01_08_2021.csv")
# file_path = os.path.abspath("cams_01_07_2021.csv")

if __name__ == "__main__":

    # load
    df = pd.read_csv(file_path, header=None, delimiter=",", usecols=[0, 1, 2], names=["date", "amount", "description"], parse_dates=['date'], dayfirst=True)

    monthly_amount_sum = df.resample('M', on='date').amount.sum()
    weekly_amount_sum = df.resample('W', on='date').amount.sum()
    daily_amount_sum = df.resample('D', on='date').amount.sum()

    cal = MyCalendar(daily_amount_sum, 7, 2021)

    with open("calendar.html", "w") as f:
        f.write("""
        <!DOCTYPE html>
        <html>
        <head>
          <link rel="stylesheet" href="styles.css">
        </head>
        <body>
        """)
        f.write(cal.formatmonth(2021, 7))
        f.write("""
        </body>
        </html>
        """)



