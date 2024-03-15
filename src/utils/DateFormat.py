import datetime


class DateFormat():

    @classmethod
    def convert_date(self, date):
        return datetime.datetime.strftime(date, '%d/%m/%Y')

    @classmethod
    def convert_time(self, time):
        return time.strftime('%H:%M')