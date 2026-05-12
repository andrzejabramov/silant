from django.contrib import admin
from django.utils.html import format_html
from core.admin import SoftDeleteAdminMixin
from .models import Claim


@admin.register(Claim)
class ClaimAdmin(SoftDeleteAdminMixin, admin.ModelAdmin):
    list_display = (
        "machine",
        "failure_node",
        "failure_date",
        "status",
        "service_company",
        "get_status_badge",
    )
    list_filter = ("status", "failure_node", "service_company", "is_deleted")
    search_fields = ("machine__serial_number", "failure_description")
    readonly_fields = ("created_at", "updated_at")

    def get_status_badge(self, obj):
        """Бейдж: визуализация статуса рекламации + приоритет"""
        COLORS = {
            "open": "#D20A11",  # красный — открыта (требует внимания)
            "in_progress": "#F59E0B",  # жёлтый — в работе
            "resolved": "#10B981",  # зелёный — решена
            "closed": "#9CA3AF",  # серый — закрыта
        }
        ICONS = {"open": "🔴", "in_progress": "🟡", "resolved": "🟢", "closed": "⚪"}

        status = obj.status
        color = COLORS.get(status, COLORS["closed"])
        icon = ICONS.get(status, "⚪")
        text = obj.get_status_display()

        # Добавляем приоритет, если есть длительность простоя
        if obj.downtime_days and obj.downtime_days > 30:
            text += " (>30 дн.)"

        return format_html(
            '<span style="background:{}; color:white; padding:4px 12px; border-radius:20px; font-size:0.8rem; font-weight:500; white-space:nowrap;">{} {}</span>',
            color,
            icon,
            text,
        )

    get_status_badge.short_description = "Визуальный статус"
