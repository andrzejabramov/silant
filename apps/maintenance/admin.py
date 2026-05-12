from django.contrib import admin
from core.admin import SoftDeleteAdminMixin
from django.utils.html import format_html
from django.utils import timezone
from .models import Maintenance


@admin.register(Maintenance)
class MaintenanceAdmin(SoftDeleteAdminMixin, admin.ModelAdmin):
    list_display = (
        "machine",
        "maintenance_type",
        "maintenance_date",
        "service_company",
        "get_status_badge",
    )
    list_filter = ("maintenance_type", "service_company", "is_deleted")
    search_fields = ("machine__serial_number", "work_order_number")
    readonly_fields = ("created_at", "updated_at")

    def get_status_badge(self, obj):
        """Бейдж: актуальность ТО"""
        COLORS = {
            "success": "#10B981",
            "warning": "#F59E0B",
            "danger": "#D20A11",
            "neutral": "#9CA3AF",
        }

        today = timezone.now().date()
        days_diff = (
            (today - obj.maintenance_date).days if obj.maintenance_date else None
        )

        if not obj.maintenance_date:
            color, icon, text = COLORS["neutral"], "—", "Нет даты"
        elif days_diff < 0:
            color, icon, text = COLORS["info"], "📅", "Запланировано"
        elif days_diff <= 90:
            color, icon, text = COLORS["success"], "✓", "Актуально"
        elif days_diff <= 180:
            color, icon, text = COLORS["warning"], "⚠", "Пора обновить"
        else:
            color, icon, text = COLORS["danger"], "✗", "Просрочено"

        return format_html(
            '<span style="background:{}; color:white; padding:4px 12px; border-radius:20px; font-size:0.8rem; font-weight:500; white-space:nowrap;">{} {}</span>',
            color,
            icon,
            text,
        )

    get_status_badge.short_description = "Актуальность"
