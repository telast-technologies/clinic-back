from datetime import time


def range_time(start_time, end_time):
    """
    Generates a list of time intervals between start_time and end_time with an increment of one hour.

    Args:
        start_time (datetime): The starting datetime.
        end_time (datetime): The ending datetime.

    Returns:
        List[datetime]: List of datetime objects incremented by one hour.
    """
    hours = []
    current_hour = start_time.hour

    while current_hour <= end_time.hour:
        hours.append(time(hour=current_hour))
        current_hour += 1

    return hours
