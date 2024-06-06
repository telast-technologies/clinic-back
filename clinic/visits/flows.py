import logging

from viewflow.fsm import State

from clinic.invoices.models import Invoice
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

    @status.transition(source=[VisitStatus.BOOKED], target=VisitStatus.CHECKED_IN)
    def check_in(self):
        logger.info(f"Checking in {self.visit}")

    @status.transition(source=[VisitStatus.CHECKED_IN], target=VisitStatus.FINANCIALLY_CLEARED)
    def financially_clear(self):
        Invoice.objects.get_or_create(visit=self.visit)
        logger.info(f"Finanicially clearing {self.visit}")

    @status.transition(source=[VisitStatus.FINANCIALLY_CLEARED], target=VisitStatus.CHECKED_OUT)
    def check_out(self):
        logger.info(f"Checking out {self.visit}")

    @status.transition(source=[VisitStatus.BOOKED, VisitStatus.CHECKED_IN], target=VisitStatus.CANCELLED)
    def cancel(self, reason):
        self.visit.comment = reason
        logger.info(f"Canceling {self.visit}")
