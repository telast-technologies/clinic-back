import logging

from django.utils import timezone
from sequences import get_next_value
from viewflow.fsm import State

from clinic.invoices.models import Invoice
from clinic.staff.models import Staff
from clinic.utils.notifications import send_inbox
from clinic.visits.choices import VisitStatus

logger = logging.getLogger(__name__)


class VisitFlow:
    status = State(VisitStatus.choices, default=VisitStatus.BOOKED)

    def __init__(self, visit):
        self.visit = visit

    @status.setter()
    def _set_status(self, value):
        self.visit.status = value

    @status.getter()
    def _get_status(self):
        return self.visit.status

    @status.on_success()
    def _on_transition_success(self, descriptor, source, target, *args, **kwargs):
        self.visit.save()

    @status.transition(source=[VisitStatus.BOOKED], target=VisitStatus.ARRIVED)
    def arrive(self, purpose):
        today = timezone.now().date()
        self.visit.arrival_info = {
            "purpose": purpose,
            "date": f"{today}",
            "queue": get_next_value(f"{today}-{self.visit.patient.clinic.pk}-{purpose}"),
        }
        Invoice.objects.get_or_create(visit=self.visit)

        logger.info(f"Arriving {self.visit}")

    @status.transition(source=[VisitStatus.ARRIVED], target=VisitStatus.CHECKED_IN)
    def check_in(self):
        logger.info(f"Checking in {self.visit}")

    @status.transition(source=[VisitStatus.CHECKED_IN], target=VisitStatus.CHECKED_OUT)
    def check_out(self):
        clinic = self.visit.patient.clinic
        admin_staff_emails = list(
            Staff.objects.filter(clinic=clinic, is_client_admin=True).values_list("user__email", flat=True)
        )

        for charge_item in self.visit.invoice.charge_items.all():
            if charge_item.supply.remains < clinic.limit_threshold:
                send_inbox(
                    charge_item.supply,
                    recipient_list=admin_staff_emails,
                    title=f"Low supply for {charge_item.supply.item}",
                    message=f"Please restock {charge_item.supply.item}",
                )

        logger.info(f"Checking out {self.visit}")

    @status.transition(source=[VisitStatus.BOOKED, VisitStatus.CHECKED_IN], target=VisitStatus.CANCELLED)
    def cancel(self, reason):
        self.visit.comment = reason
        logger.info(f"Canceling {self.visit}")
