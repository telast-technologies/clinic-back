from django.contrib import admin
from django.http import HttpRequest

from clinic.invoices.models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("visit", "tax", "discount", "sub_total", "total", "balance")
    readonly_fields = ["total", "balance"]
    search_fields = ["visit__uid"]
    
    @admin.display(description="balance")
    def balance(self, obj):
        return obj.balance
    
    @admin.display(description="total")
    def total(self, obj):
        return obj.total
    
    def has_add_permission(self, request: HttpRequest, obj: Invoice = None) -> bool:
        return False
    
    def has_change_permission(self, request: HttpRequest, obj: Invoice = None) -> bool:
        return False
    
    def has_delete_permission(self, request: HttpRequest, obj: Invoice = None) -> bool:
        return False
    