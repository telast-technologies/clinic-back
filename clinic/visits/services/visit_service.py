from django.db import transaction


class VisitService:
    def __init__(self, visit):
        self.visit = visit

    @transaction.atomic
    def check_in(self):
        self.visit.check_in()
        self.visit.save()

    @transaction.atomic
    def financially_clear(self):
        self.visit.financially_clear()
        self.visit.save()

    @transaction.atomic
    def check_out(self):
        self.visit.check_out()
        self.visit.save()

    @transaction.atomic
    def cancel(self):
        self.visit.cancel()
        self.visit.save()
