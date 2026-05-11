from django.contrib import admin
from core.admin import SoftDeleteAdminMixin
from .models import Organization

@admin.register(Organization)
class OrganizationAdmin(SoftDeleteAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'contact_email', 'phone', 'status_badge')
    search_fields = ('name', 'contact_email')
