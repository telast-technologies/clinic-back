from django.db import models
from django.db.models import F, Sum, Value
from django.db.models.functions import Coalesce


class SupplyQuerySet(models.QuerySet):
    def with_remains(self):
        return self.annotate(
            charge_quantity=Coalesce(Sum("charge_items__quantity"), Value(0.0)),
            remain=F("quantity") - F("charge_quantity"),
        ).order_by("-created_at")

    def query_remains(self, *args, **kwargs):
        return self.with_remains().filter(**kwargs)


class SupplyManager(models.Manager):
    def get_queryset(self):
        return SupplyQuerySet(self.model, using=self._db)

    def query_remains(self, *args, **kwargs):
        return self.get_queryset().query_remains(*args, **kwargs)
