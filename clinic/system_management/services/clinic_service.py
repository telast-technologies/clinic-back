import calendar
import logging
from datetime import time

from django.db import transaction
from django.db.models import Count, Value
from django.db.models.functions import Coalesce, ExtractHour

from clinic.utils.functions import range_time
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
                status__in=[VisitStatus.BOOKED],
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
        available_hours_set = set()
        dow = date.weekday()
        weekday_name = calendar.day_name[dow]

        # Retrieve all time slots for the given weekday
        slots = self.clinic.time_slots.filter(days__icontains=weekday_name)

        # Generate all possible times for the slots
        for slot in slots:
            available_hours_set.update(time.hour for time in range_time(slot.start_time, slot.end_time))

        # Fetch all scheduled visits for the date in one query
        scheduled_visits = Visit.objects.filter(
            patient__clinic=self.clinic,
            date=date,
            time__hour__in=available_hours_set,
            visit_type=VisitType.SCHEDULED,
            status__in=[VisitStatus.BOOKED],
        )

        # Annotate the visits with the hour and count the number of visits per hour
        hourly_visits = (
            scheduled_visits.annotate(hour=ExtractHour("time"))
            .values("hour")
            .annotate(count=Coalesce(Count("uid"), Value(0)))
        )
        # Create a dictionary to hold the count of visits per hour, initialized to 0
        hourly_visits_dict = {hour: 0 for hour in available_hours_set}
        # Update the dictionary with actual counts from the query
        for visit in hourly_visits:
            hourly_visits_dict[visit["hour"]] = visit["count"]

        # Prepare the final result ensuring all hours in available_hours_set are included
        available_slots = [
            time(hour=hour) for hour, count in hourly_visits_dict.items() if count < self.clinic.capacity
        ]

        # Sort the available slots by hour
        available_slots.sort()
        # return available slots
        return available_slots
