from frappe.utils import get_first_day, get_last_day
from datetime import datetime


def get_sart_and_end_date_of_month(month:int=None, year:int=None):
    '''
    if month or year is None will return the current month or it will return the 
    given month and year date
    '''
    if month is None or year is None:
        return get_first_day(), get_last_day()

    # Create a datetime object for the specified month and year
    date_object = datetime(year, month, 1)

    # Get the start date and end date of the specified month and year
    start_date = get_first_day(date_object)
    end_date = get_last_day(date_object)

    return start_date, end_date