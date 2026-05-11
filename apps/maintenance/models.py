from django.db import models
from core.models import BaseModel

class Maintenance(BaseModel):
    machine = models.ForeignKey('machines.Machine', on_delete=models.CASCADE, related_name='maintenance_records', verbose_name="Машина")
    maintenance_type = models.ForeignKey('references.MaintenanceType', on_delete=models.PROTECT, verbose_name="Вид ТО")
    maintenance_date = models.DateField(db_index=True, verbose_name="Дата проведения ТО")
    operating_hours = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Наработка, м/час")
    work_order_number = models.CharField(max_length=100, unique=True, blank=True, null=True, verbose_name="№ заказ-наряда")
    work_order_date = models.DateField(blank=True, null=True, verbose_name="Дата заказ-наряда")
    service_company = models.ForeignKey('organizations.Organization', on_delete=models.PROTECT, verbose_name="Сервисная компания")

    class Meta:
        verbose_name = "Техническое обслуживание"
        verbose_name_plural = "ТО"
        ordering = ['-maintenance_date']

    def __str__(self):
        return f"ТО {self.maintenance_type} | {self.machine.serial_number} | {self.maintenance_date}"