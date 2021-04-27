from datetime import datetime


class Dates:
    @staticmethod
    def get_current_date():
        """Returns current date in date-time format"""
        current_date = datetime.today()
        return current_date

    def str_to_date(self, string_date, date_format):
        """Format string to date (for dates passed from json or other files"""
        my_date = datetime.strptime(string_date, date_format).date()
        return my_date

    def format_date(self, some_date, date_format):
        """Formats date in datetime to required date format. Format is configurable"""
        formatted = datetime.strftime(some_date, date_format)
        return formatted

    def days_delta(self, my_date):
        """Calculates number of days between current date and user date"""
        curr_date = self.get_current_date().date()
        delta = (my_date - curr_date).days
        return delta

