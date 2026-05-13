# apps/core/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone


class SoftDeleteAdminMixin:
    """Миксин для поддержки soft delete в Django Admin"""

    actions = ["restore_selected", "hard_delete_selected"]

    # 👇 Добавляем status_badge в list_display через этот атрибут
    # (каждый ModelAdmin должен добавить 'status_badge' в свой list_display)

    @admin.display(description="Статус", ordering="is_deleted")
    def status_badge(self, obj):
        """Визуальный индикатор: ✅ Активно / 🗑 Удалено"""
        if obj.is_deleted:
            # 🔹 FIX: format_html требует {} + аргумент, либо использовать mark_safe
            return format_html(
                '<span style="color:#D20A11; font-weight:500;">🗑 {}</span>', "Удалено"
            )
        return format_html(
            '<span style="color:#163E6C; font-weight:500;">✅ {}</span>', "Активно"
        )

    @admin.action(description="Восстановить выбранные", permissions=["change"])
    def restore_selected(self, request, queryset):
        """Soft-restore: ставит is_deleted=False"""
        updated = queryset.update(is_deleted=False, updated_at=timezone.now())
        self.message_user(request, f"Восстановлено записей: {updated}")

    @admin.action(
        description="Физически удалить (безвозвратно)", permissions=["delete"]
    )
    def hard_delete_selected(self, request, queryset):
        """Hard delete: вызывает model.hard_delete() для каждой записи"""
        count = queryset.count()
        for obj in queryset:
            obj.hard_delete()  # Вызывает super().delete(), обходя менеджер
        self.message_user(request, f"Физически удалено записей: {count}")
