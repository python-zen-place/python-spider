from datetime import datetime


def get_tomorrow_week_number():
    return (datetime.today().day - datetime(2019, 9, 2).day + 1) // 7 + 1


def get_tomorrow_weekday():
    """
    we add one to get tomorrow weekday.
    but since the param start with 1, we should add one to correct offset
    :return:
    """
    return (datetime.today().weekday() + 1 + 1) % 7
