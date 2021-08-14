from calendar import HTMLCalendar
from datetime import datetime

from dateutil.relativedelta import relativedelta
from pandas import DataFrame

from constants import ACC_COL_DELIMITER, DAILY_TRANSACTIONS_DELIMITER


class SpendCalendar(HTMLCalendar):
    """Subclasses HTMLCalendar to inject our data and to manipulate the html"""

    def __init__(self, data: DataFrame, year: int, month: int, *args, **kwargs):
        self.data = data
        self.year = year
        self.month = month

        super().__init__(*args, **kwargs)

    def formatday(self, day: int, weekday: int):

        cell_html = super(SpendCalendar, self).formatday(day, weekday)

        # day will be 0 for days not in the month specified
        if day != 0:

            try:
                daily_amount = self.data["amount"][
                    f"{self.year}-{self.month}-{day}"
                ].round(decimals=2)
                daily_transactions = self.data["transactions"][
                    f"{self.year}-{self.month}-{day}"
                ]
                normalized_daily_amount = self.data["normalized_amount"][
                    f"{self.year}-{self.month}-{day}"
                ]
                transactions_list = self.get_transactions_list(daily_transactions)
                cell_colour = self.get_cell_colour(normalized_daily_amount)
            # we could get a KeyError from accessing the data frame with a date that does not
            # exist and a ValueError from splitting the daily_transactions in get_transactions_list
            except (KeyError, ValueError):
                daily_amount = 0
                transactions_list = "You have not spent anything today"
                cell_colour = self.get_cell_colour(0)

            # reconstruct the cell's html
            day_name = cell_html.split('"')[1]
            cell_html = f"""
            <td class={day_name} style="background-color:{cell_colour}">
                {day}<div>{str(daily_amount)}</div>
                <div class="transactions-tooltip">{transactions_list}</div>
            </td>"""

        return cell_html

    def get_cell_colour(self, normalized_daily_amount):
        """Display a red or a green if we've spent or gained money respectively.
        Apply the normalized amount as a percentage in alpha channel"""
        rgb = "255,0,0" if normalized_daily_amount < 0 else "0, 255, 0"
        return f"rgba({rgb},{abs(normalized_daily_amount)})"

    def create_span_with_red_or_green_text(self, amount):
        css_class = "green" if int(amount) > 0 else "red"
        return f'<div><span class="{css_class}">{str(amount)}</span></div>'

    def get_transactions_list(self, daily_transactions: str):
        html = "<ul>"
        for transaction in daily_transactions.split(DAILY_TRANSACTIONS_DELIMITER):
            description, amount = transaction.split(ACC_COL_DELIMITER)
            amount_span = self.create_span_with_red_or_green_text(float(amount))
            html += f"<li>{description}<span class='transaction-amount'>{amount_span}</span></li>"
        html += "</ul>"
        return html

    def formatmonth(self):
        calendar_html = super(SpendCalendar, self).formatmonth(self.year, self.month)
        next_month = self.next_month_button()
        prev_month = self.previous_month_button()

        buttons_container = f"""
        <div class=buttons>
            {prev_month}
            {next_month}
        </div>"""

        return buttons_container + calendar_html

    def next_month_button(self):
        next = datetime(year=self.year, month=self.month, day=1) + relativedelta(
            months=1
        )
        url = f"/calendar/year/{next.year}/month/{next.month}"
        return self.create_button(url, "Next month")

    def previous_month_button(self):
        previous = datetime(year=self.year, month=self.month, day=1) - relativedelta(
            months=1
        )
        url = f"/calendar/year/{previous.year}/month/{previous.month}"
        return self.create_button(url, "Previous month")

    def create_button(self, url, name):
        return f"""<button onclick="window.location.href='{url}';">
          {name}
        </button>"""
