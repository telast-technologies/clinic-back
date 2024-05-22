import django_filters

from clinic.visits.choices import DaysOfWeek
from clinic.visits.models import TimeSlot


class TimeSlotFilter(django_filters.FilterSet):
    days = django_filters.MultipleChoiceFilter(field_name="days", lookup_expr="icontains", choices=DaysOfWeek.choices)

    class Meta:
        model = TimeSlot
        fields = ["start_time", "end_time", "days"]
