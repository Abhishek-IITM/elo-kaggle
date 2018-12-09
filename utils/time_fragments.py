import datetime as dt

def time_of_day_fragment(time, fragments=4):
    try:
        return (int(time.hour / (24 / fragments))+1)
    except Exception as e:
        print(e)

def day_of_week(time):
    """
    :param time: datetime
    :return: day of the ween as integer
    1 is monday and 7 is sunday
    """
    try:
        return(time.date().weekday()+1)
    except Exception as e:
        print(e)

def month_from_date(time):
    """
    :param time: datetime
    :return: month num from 1 to 12
    """
    try:
        return(time.month)
    except Exception as e:
        print(e)

