from django.db import models
from core.models import BaseModel

class Machine(BaseModel):
    serial_number = models.CharField(max_length=100, unique=True, db_index=True, verbose_name="Зав. № машины")
    technique_model = models.ForeignKey('references.TechniqueModel', on_delete=models.PROTECT, verbose_name="Модель техники")
    engine_serial = models.CharField(max_length=100, blank=True, null=True, verbose_name="Зав. № двигателя")
    engine_model = models.ForeignKey('references.EngineModel', on_delete=models.PROTECT, verbose_name="Модель двигателя")
    transmission_serial = models.CharField(max_length=100, blank=True, null=True, verbose_name="Зав. № трансмиссии")
    transmission_model = models.ForeignKey('references.TransmissionModel', on_delete=models.PROTECT, verbose_name="Модель трансмиссии")
    driving_axle_serial = models.CharField(max_length=100, blank=True, null=True, verbose_name="Зав. № ведущего моста")
    driving_axle_model = models.ForeignKey('references.DrivingAxleModel', on_delete=models.PROTECT, verbose_name="Модель ведущего моста")
    steerable_axle_serial = models.CharField(max_length=100, blank=True, null=True, verbose_name="Зав. № управляемого моста")
    steerable_axle_model = models.ForeignKey('references.SteerableAxleModel', on_delete=models.PROTECT, verbose_name="Модель управляемого моста")

    supply_contract_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="№ договора поставки")
    supply_contract_date = models.DateField(blank=True, null=True, verbose_name="Дата договора")
    shipment_date = models.DateField(db_index=True, verbose_name="Дата отгрузки с завода")
    recipient = models.CharField(max_length=255, blank=True, null=True, verbose_name="Грузополучатель")
    operation_address = models.TextField(blank=True, null=True, verbose_name="Адрес эксплуатации")
    equipment_options = models.TextField(blank=True, null=True, verbose_name="Комплектация")

    client = models.ForeignKey(
        'organizations.Organization', on_delete=models.SET_NULL, null=True, blank=True, related_name='client_machines',
        verbose_name="Клиент"
    )
    service_company = models.ForeignKey(
        'organizations.Organization', on_delete=models.SET_NULL, null=True, blank=True, related_name='service_machines',
        verbose_name="Сервисная компания"
    )

    class Meta:
        verbose_name = "Машина"
        verbose_name_plural = "Машины"
        ordering = ['-shipment_date']

    def __str__(self):
        return f"{self.technique_model} ({self.serial_number})"
