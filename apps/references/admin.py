# apps/references/admin.py
from django.contrib import admin
from core.admin import SoftDeleteAdminMixin
from .models import (
    TechniqueModel,
    EngineModel,
    TransmissionModel,
    DrivingAxleModel,
    SteerableAxleModel,
    MaintenanceType,
    FailureNode,
    RestorationMethod,
)


class ReferenceAdmin(SoftDeleteAdminMixin, admin.ModelAdmin):
    """Базовый админ-класс для всех справочников"""

    list_display = ("name", "status_badge", "created_at", "updated_at")
    list_display_links = ("name",)  # Поле доступно для клика/перехода в карточку
    search_fields = ("name",)
    list_filter = ("is_deleted", "created_at")
    ordering = ("name",)  # Сортировка по алфавиту по умолчанию
    readonly_fields = ("created_at", "updated_at")  # Защита аудита от ручных правок


# Регистрация всех справочников через один класс
admin.site.register(TechniqueModel, ReferenceAdmin)
admin.site.register(EngineModel, ReferenceAdmin)
admin.site.register(TransmissionModel, ReferenceAdmin)
admin.site.register(DrivingAxleModel, ReferenceAdmin)
admin.site.register(SteerableAxleModel, ReferenceAdmin)
admin.site.register(MaintenanceType, ReferenceAdmin)
admin.site.register(FailureNode, ReferenceAdmin)
admin.site.register(RestorationMethod, ReferenceAdmin)
