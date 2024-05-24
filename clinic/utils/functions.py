from datetime import time


def generate_hourly_range(start_time, end_time):
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
        hours.append(current_hour)
        current_hour += 1

    return hours


def convert_hours_to_times(hours):
    """
    Convert an array of integers representing hours into a list of datetime.time objects.

    Args:
        hours (list): A list of integers representing hours (0-23).

    Returns:
        list: A list of datetime.time objects corresponding to the input hours.
    """
    return [time(hour=h) for h in hours]
