import datetime


def get_next_weekday(weekday: int) -> datetime:
    today = datetime.date.today()
    weekday = today + datetime.timedelta((weekday - today.weekday()) % 7)
    # make sure to zero the time
    return datetime.datetime(weekday.year, weekday.month, weekday.day)

def string_to_datetime(string_date) -> datetime:
    return datetime.datetime.strptime(string_date, '%Y%m%d')