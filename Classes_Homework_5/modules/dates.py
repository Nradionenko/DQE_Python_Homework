from datetime import datetime


class Dates:
    def __init__(self, date_format, datetime_format):
        self.date_format = date_format
        self.datetime_format = datetime_format

    @staticmethod
    def get_current_date():
        """Returns current date in date-time format"""
        current_date = datetime.today()
        return current_date

    def format_date(self, some_date):
        """Formats date in datetime to required date format. Format is configurable"""
        formatted = datetime.strftime(some_date, self.date_format)
        return formatted

    def format_date_time(self, some_date):
        """Formats date in datetime to required datetime format. Format is configurable"""
        formatted = datetime.strftime(some_date, self.datetime_format)
        return formatted

    def days_delta(self, my_date):
        """Calculates number of days between current date and user date"""
        curr_date = self.get_current_date().date()
        delta = (my_date - curr_date).days
        return delta
