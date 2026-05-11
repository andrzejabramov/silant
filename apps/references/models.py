from django.db import models
from core.models import BaseModel

class BaseReference(BaseModel):
    name = models.CharField(max_length=255, unique=True, db_index=True, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class TechniqueModel(BaseReference):
    class Meta:
        verbose_name = "Модель техники"
        verbose_name_plural = "Модели техники"

class EngineModel(BaseReference):
    class Meta:
        verbose_name = "Модель двигателя"
        verbose_name_plural = "Модели двигателей"

class TransmissionModel(BaseReference):
    class Meta:
        verbose_name = "Модель трансмиссии"
        verbose_name_plural = "Модели трансмиссий"

class DrivingAxleModel(BaseReference):
    class Meta:
        verbose_name = "Модель ведущего моста"
        verbose_name_plural = "Модели ведущих мостов"

class SteerableAxleModel(BaseReference):
    class Meta:
        verbose_name = "Модель управляемого моста"
        verbose_name_plural = "Модели управляемых мостов"

class MaintenanceType(BaseReference):
    class Meta:
        verbose_name = "Вид ТО"
        verbose_name_plural = "Виды ТО"

class FailureNode(BaseReference):
    class Meta:
        verbose_name = "Узел отказа"
        verbose_name_plural = "Узлы отказа"

class RestorationMethod(BaseReference):
    class Meta:
        verbose_name = "Способ восстановления"
        verbose_name_plural = "Способы восстановления"
