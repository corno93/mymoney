
import os
import pandas as pd

"""
Stupid script to read combank csv and output monthly spend

cols:
date, amount, description, acc total (smart access)

("""


file_path = os.path.abspath("01_01_2021_to_01_08_2021.csv")


if __name__ == "__main__":

    # load
    df = pd.read_csv(file_path, header=None, delimiter=",", usecols=[0, 1, 2], names=["date", "amount", "description"], parse_dates=['date'], dayfirst=True)

    monthly_amount_sum = df.resample('M', on='date').amount.sum()
    weekly_amount_sum = df.resample('W', on='date').amount.sum()
    daily_amount_sum = df.resample('D', on='date').amount.sum()
    g = 1

