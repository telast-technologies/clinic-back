import calendar
import logging
from datetime import time

from django.db import transaction
from django.db.models import Count, Value
from django.db.models.functions import Coalesce, ExtractHour
from django.utils.translation import gettext_lazy as _

from clinic.visits.choices import VisitStatus, VisitType
from clinic.visits.models import Visit

logger = logging.getLogger(__name__)


class ClinicService:
    def __init__(self, clinic):
        self.clinic = clinic

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
        try:
            available_hours_set = set()
            dow = date.weekday()
            weekday_name = calendar.day_name[dow]

            # Retrieve all time slots for the given weekday
            slots = self.clinic.time_slots.filter(days__icontains=weekday_name)

            # Generate all possible times for the slots
            available_hours_set.update(
                slot_hour for slot in slots for slot_hour in range(slot.start_time.hour, slot.end_time.hour)
            )
            # Fetch all scheduled visits for the date in one query
            scheduled_visits = Visit.objects.filter(
                patient__clinic=self.clinic,
                date=date,
                time__hour__in=available_hours_set,
                visit_type=VisitType.SCHEDULED,
                status__in=[VisitStatus.BOOKED],
            ).prefetch_related("patient")
            # Annotate the visits with the hour and count the number of visits per hour
            hourly_visits = (
                scheduled_visits.annotate(hour=ExtractHour("time"))
                .values("hour")
                .annotate(count=Coalesce(Count("uid"), Value(0)))
            )
            # Create a dictionary to hold the count of visits per hour, initialized to 0
            hourly_visits_dict = {visit["hour"]: visit["count"] for visit in hourly_visits}
            # Update the dictionary with actual counts from the query
            hourly_visits_dict.update({hour: 0 for hour in available_hours_set if hour not in hourly_visits_dict})

            # Prepare the final result ensuring all hours in available_hours_set are included
            # Sort the available slots by hour
            available_slots = sorted(
                [time(hour=hour) for hour, count in hourly_visits_dict.items() if count < self.clinic.capacity]
            )
            # return available slots
            return available_slots

        except Exception as e:
            logger.error("Error checking get available slot: %s", e)
            raise Exception(_(str(e)))
