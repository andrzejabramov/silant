# apps/organizations/admin.py
from django.contrib import admin
from django.utils.html import format_html
from core.admin import SoftDeleteAdminMixin
from .models import Organization


@admin.register(Organization)
class OrganizationAdmin(SoftDeleteAdminMixin, admin.ModelAdmin):
    # 🔹 Добавляем флаги в список отображения + сохраняем статус
    list_display = (
        "name",
        "is_buyer",  # 👈 Покупатель
        "is_client",  # 👈 Клиент
        "is_service_company",  # 👈 Сервис
        "contact_email",
        "phone",
        "get_status_badge",  # 👈 Сохраняем твой бейдж с количеством машин
    )

    # 🔹 Фильтры справа в админке
    list_filter = (
        "is_buyer",
        "is_client",
        "is_service_company",
        "is_deleted",  # Из миксина SoftDelete
    )

    # 🔹 Редактирование флагов прямо в списке (галочки)
    list_editable = ("is_buyer", "is_client", "is_service_company")

    search_fields = ("name", "contact_email")
    ordering = ("name",)

    def get_queryset(self, request):
        # 👈 Показываем и удалённые записи, чтобы можно было восстановить
        # Используем all_objects из BaseModel, чтобы обойти SoftDeleteManager
        return Organization.all_objects.all()

    def get_status_badge(self, obj):
        """Бейдж: количество машин + статус активности (твой код без изменений)"""
        COLORS = {"success": "#10B981", "warning": "#F59E0B", "neutral": "#9CA3AF"}

        # Безопасный подсчёт связанных машин (через related_name из Machine.client/service_company)
        machine_count = 0
        if hasattr(obj, "client_machines"):
            machine_count += obj.client_machines.filter(is_deleted=False).count()
        if hasattr(obj, "service_machines"):
            machine_count += obj.service_machines.filter(is_deleted=False).count()

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
