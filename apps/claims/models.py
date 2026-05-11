from django.db import models
from core.models import BaseModel

class Claim(BaseModel):
    STATUS_OPEN = 'open'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_RESOLVED = 'resolved'
    STATUS_CHOICES = [
        (STATUS_OPEN, 'Открыта'),
        (STATUS_IN_PROGRESS, 'В работе'),
        (STATUS_RESOLVED, 'Закрыта'),
    ]

    machine = models.ForeignKey('machines.Machine', on_delete=models.CASCADE, related_name='claims', verbose_name="Машина")
    failure_date = models.DateField(db_index=True, verbose_name="Дата отказа")
    operating_hours = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Наработка, м/час")
    failure_node = models.ForeignKey('references.FailureNode', on_delete=models.PROTECT, verbose_name="Узел отказа")
    failure_description = models.TextField(verbose_name="Описание отказа")
    restoration_method = models.ForeignKey('references.RestorationMethod', on_delete=models.PROTECT, verbose_name="Способ восстановления")
    spare_parts_used = models.TextField(blank=True, null=True, verbose_name="Используемые запасные части")
    restoration_date = models.DateField(blank=True, null=True, verbose_name="Дата восстановления")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_OPEN, verbose_name="Статус")
    service_company = models.ForeignKey('organizations.Organization', on_delete=models.PROTECT, verbose_name="Сервисная компания")

    class Meta:
        verbose_name = "Рекламация"
        verbose_name_plural = "Рекламации"
        ordering = ['-failure_date']

    def __str__(self):
        return f"Рекламация {self.failure_node} | {self.machine.serial_number}"

    @property
    def downtime_days(self):
        if self.restoration_date and self.failure_date:
            return (self.restoration_date - self.failure_date).days
        return None
