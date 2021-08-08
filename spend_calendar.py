from calendar import HTMLCalendar


class SpendCalendar(HTMLCalendar):
    """Subclasses HTMLCalendar to inject more information:
    - daily total spend
    - prev, next month buttons"""

    def __init__(self, daily_amount_sum, year, month, *args, **kwargs):
        self.daily_amount_sum = daily_amount_sum
        self.year = year
        self.month = month

        super().__init__(*args, **kwargs)

    def formatday(self, day, weekday):

        day_html = super(SpendCalendar, self).formatday(day, weekday)

        if day != 0:

            try:
                daily_amount = self.daily_amount_sum[f"{self.year}-{self.month}-{day}"]
            except KeyError:
                daily_amount = 0

            # inject new data
            div_class = "green" if daily_amount > 0 else "red"
            amount_div = f'<div class="{div_class}">{str(daily_amount)}</div>'
            day_html = f"{day_html[:-5]}{amount_div}</td>"

        return day_html

    def formatmonth(self):
        calendar_html = super(SpendCalendar, self).formatmonth(self.year, self.month)
        next_month = self.next_month_button()
        prev_month = self.previous_month_button()

        buttons_container = f"""
        <div class=buttons>
            {next_month}
            {prev_month}
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
