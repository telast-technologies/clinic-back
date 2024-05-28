from django.db import transaction

from clinic.visits.flows import VisitFlow


class VisitService:
    def __init__(self, visit):
        self.visit = visit
        self.flow = VisitFlow(self.visit)

    @transaction.atomic
    def check_in(self):
        self.flow.check_in()

    @transaction.atomic
    def financially_clear(self):
        self.flow.financially_clear()

    @transaction.atomic
    def check_out(self):
        self.flow.check_out()

    @transaction.atomic
    def cancel(self):
        self.flow.cancel()
