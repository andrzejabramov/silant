from django.contrib import admin
from core.admin import SoftDeleteAdminMixin
from .models import (
    TechniqueModel, EngineModel, TransmissionModel,
    DrivingAxleModel, SteerableAxleModel, MaintenanceType,
    FailureNode, RestorationMethod
)

class ReferenceAdmin(SoftDeleteAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'status_badge')
    search_fields = ('name',)

admin.site.register(TechniqueModel, ReferenceAdmin)
admin.site.register(EngineModel, ReferenceAdmin)
admin.site.register(TransmissionModel, ReferenceAdmin)
admin.site.register(DrivingAxleModel, ReferenceAdmin)
admin.site.register(SteerableAxleModel, ReferenceAdmin)
admin.site.register(MaintenanceType, ReferenceAdmin)
admin.site.register(FailureNode, ReferenceAdmin)
admin.site.register(RestorationMethod, ReferenceAdmin)
