import calendar
import logging
from collections import defaultdict

from django.db import transaction

from clinic.utils.functions import generate_hourly_range
from clinic.visits.choices import VisitStatus, VisitType
from clinic.visits.models import Visit

logger = logging.getLogger(__name__)


class ClinicService:
    def __init__(self, clinic):
        self.clinic = clinic

    @transaction.atomic
    def valid_slot(self, date, time):
        """
        Check if a given date and time slot is valid and available in the clinic schedule.

        Args:
            date (datetime.date): The date to check for availability.
            time (datetime.time): The specific time to check for availability.

        Returns:
            bool: True if the slot is valid and available, False otherwise.
        """
        try:
            dow = date.weekday()
            weekday_name = calendar.day_name[dow]

            # Check if the time slot is valid for the given day
            slots = self.clinic.time_slots.filter(
                days__icontains=weekday_name, start_time__lte=time, end_time__gte=time
            )

            # Count the number of visits scheduled for the given date and time
            visits_count = Visit.objects.filter(
                patient__clinic=self.clinic,
                date=date,
                time=time,
                visit_type=VisitType.SCHEDULED,
                status__in=[VisitStatus.BOOKED, VisitStatus.CHECKED_IN],
            ).count()

            return slots.exists() and visits_count <= self.clinic.capacity

        except Exception as e:
            # Log the exception here if logging is configured
            # logger.error(f"Error checking valid slot: {e}")
            logger.error("Error checking valid slot: %s", e)
            return False

    @transaction.atomic
    def get_available_slots(self, date):
        """
        Retrieve available time slots for a given date by checking the clinic's schedule
        and existing appointments.

        Args:
            date (datetime.date): The date for which to retrieve available time slots.

        Returns:
            list: A list of available time slots for the given date.
        """
        times = []
        dow = date.weekday()
        weekday_name = calendar.day_name[dow]

        # Retrieve all time slots for the given weekday
        slots = self.clinic.time_slots.filter(days__icontains=weekday_name)

        # Generate all possible times for the slots
        for slot in slots:
            times += generate_hourly_range(slot.start_time, slot.end_time)

        # Convert times to a set to ensure unique values
        available_times_set = set(times)

        # Fetch all scheduled visits for the date in one query
        scheduled_visits = Visit.objects.filter(patient__clinic=self.clinic, date=date, visit_type=VisitType.SCHEDULED)

        # Create a dictionary to count the number of visits for each time
        visit_counts = defaultdict(int)
        for visit in scheduled_visits:
            visit_time = visit.time.hour
            if visit_time in available_times_set:
                visit_counts[visit_time] += 1

        # Filter out times where the clinic is at capacity
        available_times = [time for time in available_times_set if visit_counts[time] < self.clinic.capacity]

        return available_times
