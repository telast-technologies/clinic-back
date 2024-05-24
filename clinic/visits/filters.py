import django_filters

from clinic.visits.choices import DaysOfWeek
from clinic.visits.models import ChargeItem, ChargeService, TimeSlot, Visit


class TimeSlotFilter(django_filters.FilterSet):
    days = django_filters.MultipleChoiceFilter(field_name="days", lookup_expr="icontains", choices=DaysOfWeek.choices)

    class Meta:
        model = TimeSlot
        fields = ["start_time", "end_time", "days"]


class VisitFilter(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter(field_name="date")
    time_after = django_filters.NumberFilter(lookup_expr="gte", field_name="created_at__hour")
    time_before = django_filters.NumberFilter(lookup_expr="lte", field_name="created_at__hour")

    class Meta:
        model = Visit
        fields = ["patient", "date", "time_after", "time_before", "status", "visit_type"]


class SelectVisitFilter(django_filters.FilterSet):
    class Meta:
        model = Visit
        fields = ["uid"]


class ChargeItemFilter(django_filters.FilterSet):
    visit = django_filters.ModelChoiceFilter(queryset=Visit.objects.all(), field_name="visit", required=True)

    class Meta:
        model = ChargeItem
        fields = ["uid", "visit", "supply"]


class ChargeServiceFilter(django_filters.FilterSet):
    visit = django_filters.ModelChoiceFilter(queryset=Visit.objects.all(), field_name="visit", required=True)

    class Meta:
        model = ChargeService
        fields = ["uid", "visit", "service"]
