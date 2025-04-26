import pandas as pd
from django.db.models import Count
from django.utils import timezone
from rest_pandas import PandasSimpleView, PandasView

from clinic.invoices.choices import InvoiceStatus
from clinic.invoices.models import ChargeService, Invoice
from clinic.patients.api.v1.serializers import PatientSerializer
from clinic.patients.models import Patient
from clinic.users.abstracts.mixins import QuerysetFilteredMixin
from clinic.users.api.permissions import IsAdminStaff
from clinic.visits.models import Visit


class VisitDashboardView(PandasSimpleView):
    """
    View for the visit dashboard.
    """

    permission_classes = [IsAdminStaff]

    def get_data(self, request, start_date, end_date, *args, **kwargs):
        # get the current clinic
        current_clinic = request.user.staff.clinic
        # supplies
        supplies_below_threshold = current_clinic.supplies.query_remains(remain__lte=current_clinic.limit_threshold)
        expires_soon = current_clinic.supplies.filter(expires_at__lt=timezone.now() + timezone.timedelta(days=30))

        # visits
        visits = Visit.objects.filter(date__range=(start_date, end_date))
        visit_type_distribution = list(visits.values("visit_type").annotate(count=Count("uid")))
        purpose_distribution = list(visits.values("arrival_info__purpose").annotate(count=Count("uid")))
        status_distribution = list(visits.values("status").annotate(count=Count("uid")))
        # patients
        patients = current_clinic.patients.filter(visits__date__range=(start_date, end_date))
        new_patients_count = patients.annotate(visit_count=Count("visits")).filter(visit_count=1).count()
        returning_patients_count = patients.annotate(visit_count=Count("visits")).filter(visit_count__gt=1).count()
        patient_region_distribution = list(patients.values("country").annotate(count=Count("uid")))
        patient_channel_distribution = list(patients.values("channel").annotate(count=Count("uid")))
        # services
        services_distribution = list(
            ChargeService.objects.filter(
                invoice__visit__patient__clinic=current_clinic, invoice__visit__date__range=(start_date, end_date)
            )
            .values("service__name")
            .annotate(count=Count("uid"))
        )
        # invoices
        invoices = Invoice.objects.filter(
            visit__patient__clinic=current_clinic, visit__date__range=(start_date, end_date)
        )
        total_earnings = sum([invoice.balance for invoice in invoices.filter(status=InvoiceStatus.PAID)])

        return pd.DataFrame(
            [
                {
                    "visits": {
                        "total_count": visits.count(),
                        "visit_type_distribution": visit_type_distribution,
                        "purpose_distribution": purpose_distribution,
                        "status_distribution": status_distribution,
                    },
                    "patient": {
                        "new_patients": new_patients_count,
                        "returning_patients": returning_patients_count,
                        "region_distribution": patient_region_distribution,
                        "channel_distribution": patient_channel_distribution,
                    },
                    "services": {"distribution": services_distribution},
                    "supplies": {
                        "below_threshold": supplies_below_threshold.count(),
                        "expires_soon": expires_soon.count(),
                    },
                    "invoices": {"total_earnings": total_earnings},
                }
            ]
        )


class ExportPatientsView(QuerysetFilteredMixin, PandasView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAdminStaff]
