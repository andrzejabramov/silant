from django.contrib import admin
from core.admin import SoftDeleteAdminMixin
from django.utils.html import format_html
from django.utils import timezone
from .models import Machine


@admin.register(Machine)
class MachineAdmin(SoftDeleteAdminMixin, admin.ModelAdmin):
    list_display = (
        "serial_number",
        "technique_model",
        "client",
        "shipment_date",
        "get_status_badge",
    )
    list_filter = ("technique_model", "client", "service_company", "is_deleted")
    search_fields = ("serial_number", "recipient")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "shipment_date"

    def get_status_badge(self, obj):
        """Бейдж: статус машины по бизнес-логике"""
        COLORS = {
            "success": "#10B981",
            "warning": "#F59E0B",
            "danger": "#D20A11",
            "info": "#163E6C",
            "neutral": "#9CA3AF",
        }

        # Логика статуса
        if obj.is_deleted:
            color, icon, text = COLORS["danger"], "✗", "Удалена"
        elif not obj.shipment_date:
            color, icon, text = COLORS["info"], "📦", "На складе"
        elif obj.shipment_date > timezone.now().date():
            color, icon, text = COLORS["warning"], "🚚", "В пути"
        elif obj.claims.filter(status="open").exists():
            color, icon, text = COLORS["danger"], "⚠", "Есть рекламации"
        elif obj.client:
            color, icon, text = (
                COLORS["success"],
                "✓",
                f'У {obj.client.name[:15]}{"..." if len(obj.client.name)>15 else ""}',
            )
        else:
            color, icon, text = COLORS["neutral"], "—", "Неизвестно"

        return format_html(
            '<span style="background:{}; color:white; padding:4px 12px; border-radius:20px; font-size:0.8rem; font-weight:500; white-space:nowrap;">{} {}</span>',
            color,
            icon,
            text,
        )

    get_status_badge.short_description = "Статус"
