from datetime import datetime, date, timedelta


def format_date(date_string):
    """
    Convert a date from YYYY-MM-DD to 'Mon D, YYYY' format.

    Args:
        date_string (str): Date string, e.g. '2026-11-01'.

    Returns:
        str: Formatted date, e.g. 'Nov 1, 2026'.

    Raises:
        ValueError: If the input date does not match YYYY-MM-DD
                    or represents an invalid date.

    Example:
        >>> format_date("2026-11-01")
        'Nov 1, 2026'
    """
    date = datetime.strptime(date_string, "%Y-%m-%d")
    return f"{date.strftime('%b')} {date.day}, {date.year}"


def flight_date(days=0):
    return (date.today() + timedelta(days=days)).isoformat()


def format_flight_time_of_day(flight_time):
    hour = flight_time.split(':')[0]
    minute = flight_time.split(':')[1]
    formatted_flight_time = hour + ':' + minute
    print(formatted_flight_time)
    return formatted_flight_time


def format_price(price):
    return f"${price:,.2f}"
