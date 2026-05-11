from django.contrib import admin
from core.admin import SoftDeleteAdminMixin
from .models import Machine

@admin.register(Machine)
class MachineAdmin(SoftDeleteAdminMixin, admin.ModelAdmin):
    list_display = ('serial_number', 'technique_model', 'client', 'shipment_date', 'status_badge')
    list_filter = ('technique_model', 'client', 'service_company', 'is_deleted')
    search_fields = ('serial_number', 'recipient')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'shipment_date'
