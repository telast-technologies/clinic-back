import django_filters
from django.db.models import Q
from django.utils import timezone

from clinic.visits.choices import DaysOfWeek, TimeChoices
from clinic.visits.models import TimeSlot, Visit


class TimeSlotFilter(django_filters.FilterSet):
    days = django_filters.MultipleChoiceFilter(field_name="days", lookup_expr="icontains", choices=DaysOfWeek.choices)

    class Meta:
        model = TimeSlot
        fields = ("start_time", "end_time", "days")


class VisitFilter(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter(field_name="date")
    time = django_filters.ChoiceFilter(method="filter_time", choices=TimeChoices.choices, label="Filter by visit time")

    class Meta:
        model = Visit
        fields = ("patient", "date", "time", "status", "visit_type")

    def filter_time(self, queryset, name, value):
        now = timezone.now()

        if value == TimeChoices.UPCOMING:
            queryset = queryset.filter(Q(Q(date=now.date()), Q(time__gte=now.time())) | Q(date__gt=now.date()))
        if value == TimeChoices.PAST:
            queryset = queryset.filter(date__lte=now.date(), time__lt=now.time())

        return queryset


class SelectVisitFilter(django_filters.FilterSet):
    class Meta:
        model = Visit
        fields = ("uid", "status")
