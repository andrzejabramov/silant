from django.contrib import admin
from core.admin import SoftDeleteAdminMixin
from .models import Claim

@admin.register(Claim)
class ClaimAdmin(SoftDeleteAdminMixin, admin.ModelAdmin):
    list_display = ('machine', 'failure_node', 'failure_date', 'status', 'service_company', 'status_badge')
    list_filter = ('status', 'failure_node', 'service_company', 'is_deleted')
    search_fields = ('machine__serial_number', 'failure_description')
    readonly_fields = ('created_at', 'updated_at')
