import calendar
import logging
from datetime import date, time, timedelta

from django.db import transaction
from django.db.models import Count

from clinic.visits.choices import VisitStatus, VisitType
from clinic.visits.models import Visit

logger = logging.getLogger(__name__)


class ClinicService:
    def __init__(self, clinic):
        self.clinic = clinic

    def get_available_dates(self, patient_id: int) -> list[date]:
        """
        Get the available dates for a patient's visits.

        This method retrieves the available dates for a patient's visits within the next 31 days.
        It does this by querying the `Visit` model for visits of the specified patient that
        are scheduled within the next 31 days and belong to the current clinic.

        Args:
            patient_id (int): The ID of the patient.

        Returns:
            List[date]: A list of available dates for the patient's visits.
        """
        # Get today's date
        today: date = date.today()

        # Generate a list of the next 31 days
        available_dates: list[date] = [today + timedelta(days=i) for i in range(31)]
        # Query the Visit model for visits of the specified patient that are scheduled within
        # the next 31 days and belong to the current clinic
        booked_dates: list[date] = (
            Visit.objects.filter(
                patient_id=patient_id,  # Filter by patient ID
                patient__clinic=self.clinic,  # Filter by current clinic
                date__in=available_dates,  # Filter by date within the next 31 days
            )
            .values("date")  # Group the visits by date
            .annotate(count=Count("date"))  # Count the number of visits for each date
            .values_list("date", flat=True)  # Extract the date values from the queryset
        )
        available_dates = filter(lambda date: date not in booked_dates, available_dates)
        # Return the list of available dates
        return list(available_dates)

    @transaction.atomic
    def get_available_slots(self, date: date) -> list[time]:
        """
        Get available time slots for a given date by checking the clinic's schedule
        and existing appointments.

        Args:
            date (datetime.date): The date for which to retrieve available time slots.

        Returns:
            List[time]: A list of available time slots for the given date.
        """
        day_of_week = date.weekday()
        available_hours = self.clinic.slots.get(calendar.day_name[day_of_week].lower(), [])

        # Precompute the hourly visit counts for the clinic and date
        hourly_visits_dict = {
            hour: Visit.objects.filter(
                patient__clinic=self.clinic,
                date=date,
                time__hour=hour,
                visit_type=VisitType.SCHEDULED,
                status=VisitStatus.BOOKED,
            ).count()
            for hour in available_hours
        }

        # Filter out hours with booked visits
        available_slots = [
            time(hour=hour) for hour, count in hourly_visits_dict.items() if count < self.clinic.capacity
        ]

        return sorted(available_slots)
