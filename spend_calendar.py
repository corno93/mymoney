from calendar import HTMLCalendar


class SpendCalendar(HTMLCalendar):

    def __init__(self, daily_amount_sum, month, year, *args, **kwargs):
        self.daily_amount_sum = daily_amount_sum
        self.month = month
        self.year = year
        super().__init__(*args, **kwargs)

    def formatday(self, day, weekday):

        day_html = super(SpendCalendar, self).formatday(day, weekday)

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
