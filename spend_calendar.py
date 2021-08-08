from calendar import HTMLCalendar

from constants import ACC_COL_DELIMITER, DAILY_TRANSACTIONS_DELIMITER


class SpendCalendar(HTMLCalendar):
    """Subclasses HTMLCalendar to inject more information:
    - daily total spend
    - prev, next month buttons
    - transaction description and amount
    """

    def __init__(
        self, daily_amount_sum, daily_transactions, year, month, *args, **kwargs
    ):
        self.daily_amount_sum = daily_amount_sum
        self.daily_transactions = daily_transactions
        self.year = year
        self.month = month

        # TODO: validate that data exists for month here and handle response

        super().__init__(*args, **kwargs)

    def formatday(self, day, weekday):

        day_html = super(SpendCalendar, self).formatday(day, weekday)

        if day != 0:

            daily_amount = self.daily_amount_sum[
                f"{self.year}-{self.month}-{day}"
            ].round(decimals=2)
            daily_transactions = self.daily_transactions[
                f"{self.year}-{self.month}-{day}"
            ]

            if daily_amount:
                transactions_tooltip = self.create_transactions_tooltip(
                    daily_transactions
                )
            else:
                daily_amount = 0
                transactions_tooltip = "You have not spent anything today"

            amount_span = self.create_span_with_red_or_green_text(daily_amount)
            transactions_div = (
                f'<div class="transactions-tooltip">{transactions_tooltip}</div>'
            )

            # remove the old '</td>' and add the new content
            day_html = f"{day_html[:-5]}{amount_span}{transactions_div}</td>"

        return day_html

    def create_span_with_red_or_green_text(self, amount):
        css_class = "green" if int(amount) > 0 else "red"
        return f'<div><span class="{css_class}">{str(amount)}</span></div>'

    def create_transactions_tooltip(self, daily_transactions):
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
        if self.month == 12:
            next_month = 1
            year = self.year + 1
        else:
            next_month = self.month + 1
            year = self.year

        url = f"/calendar/year/{year}/month/{next_month}"
        return self.create_button(url, "Next month")

    def previous_month_button(self):
        if self.month == 1:
            prev_month = 12
            year = self.year - 1
        else:
            prev_month = self.month - 1
            year = self.year

        url = f"/calendar/year/{year}/month/{prev_month}"
        return self.create_button(url, "Previous month")

    def create_button(self, url, name):
        return f"""<button onclick="window.location.href='{url}';">
          {name}
        </button>"""
