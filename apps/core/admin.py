from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone

class SoftDeleteAdminMixin:
    actions = ['restore_selected', 'hard_delete_selected']

    def get_queryset(self, request):
        return self.model.all_objects.all()

    @admin.display(description='Статус')
    def status_badge(self, obj):
        if obj.is_deleted:
            return format_html('<span style="color:red;">🗑 Удалено</span>')
        return format_html('<span style="color:green;">✅ Активно</span>')

    @admin.action(description='Восстановить выбранные')
    def restore_selected(self, request, queryset):
        updated = queryset.update(is_deleted=False, updated_at=timezone.now())
        self.message_user(request, f'Восстановлено: {updated}')

    @admin.action(description='Физически удалить')
    def hard_delete_selected(self, request, queryset):
        count = queryset.count()
        for obj in queryset:
            obj.hard_delete()
        self.message_user(request, f'Физически удалено: {count}')
