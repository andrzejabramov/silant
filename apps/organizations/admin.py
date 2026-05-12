from django.contrib import admin
from django.utils.html import format_html
from core.admin import SoftDeleteAdminMixin
from .models import Organization


@admin.register(Organization)
class OrganizationAdmin(SoftDeleteAdminMixin, admin.ModelAdmin):
    list_display = ("name", "contact_email", "phone", "get_status_badge")
    search_fields = ("name", "contact_email")

    def get_status_badge(self, obj):
        """Бейдж: количество машин + статус активности"""
        COLORS = {"success": "#10B981", "warning": "#F59E0B", "neutral": "#9CA3AF"}

        machine_count = obj.machines.count() if hasattr(obj, "machines") else 0

        if machine_count == 0:
            color, icon, text = COLORS["neutral"], "—", "Нет машин"
        elif machine_count < 5:
            color, icon, text = COLORS["warning"], "⚠", f"{machine_count} машины"
        else:
            color, icon, text = COLORS["success"], "✓", f"{machine_count} машин"

        return format_html(
            '<span style="background:{}; color:white; padding:4px 12px; border-radius:20px; font-size:0.8rem; font-weight:500; white-space:nowrap;">{} {}</span>',
            color,
            icon,
            text,
        )

    get_status_badge.short_description = "Статус"
    get_status_badge.admin_order_field = "machines__count"
