from django.conf import settings
from django.contrib.auth.models import Permission
from django.core.cache import cache
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from clinic.system_management.choices import PackageChoices
from clinic.utils.models import TimestampMixin, UUIDAutoFieldMixin


class Package(UUIDAutoFieldMixin, TimestampMixin):
    name = models.CharField(max_length=100, unique=True, choices=PackageChoices.choices)
    description = models.TextField(null=True, blank=True)
    price = models.PositiveIntegerField()
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.name


class Clinic(UUIDAutoFieldMixin, TimestampMixin):
    package = models.ForeignKey("Package", on_delete=models.RESTRICT, related_name="clinics")
    logo = models.ImageField(upload_to="clinics/logos", null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    phone = PhoneNumberField(region=settings.PHONENUMBER_DEFAULT_REGION, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    capacity = models.PositiveIntegerField(_("Patient Count Capacity/Hours"), default=5)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.name

    @property
    def days(self):
        cache_key = f"clinic_days_{self.uid}"
        dow_set = cache.get(cache_key)
        if not dow_set:
            slots = self.time_slots.values_list("days", flat=True)
            dow_set = {day for sublist in slots for day in sublist}
            cache.set(cache_key, dow_set, settings.CACHE_TIMEOUT)

        return dow_set

    @property
    def slots(self):
        cache_key = f"clinic_slots_{self.uid}"
        slot_dict = cache.get(cache_key)

        if not slot_dict:
            slot_dict = dict({})
            for day in self.days:
                available_hours_set = set()
                # Retrieve all time slots for the given weekday
                slots = self.time_slots.filter(days__icontains=day)

                # Generate all possible times for the slots
                available_hours_set.update(
                    slot_hour for slot in slots for slot_hour in range(slot.start_time.hour, slot.end_time.hour + 1)
                )
                slot_dict[day] = available_hours_set

            cache.set(cache_key, slot_dict, settings.CACHE_TIMEOUT)

        return slot_dict


class ExposedPermission(UUIDAutoFieldMixin, TimestampMixin):
    permission = models.OneToOneField(Permission, on_delete=models.CASCADE)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.permission.name
