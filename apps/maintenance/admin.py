from django.contrib import admin
from core.admin import SoftDeleteAdminMixin
from .models import Maintenance

@admin.register(Maintenance)
class MaintenanceAdmin(SoftDeleteAdminMixin, admin.ModelAdmin):
    list_display = ('machine', 'maintenance_type', 'maintenance_date', 'service_company', 'status_badge')
    list_filter = ('maintenance_type', 'service_company', 'is_deleted')
    search_fields = ('machine__serial_number', 'work_order_number')
    readonly_fields = ('created_at', 'updated_at')
