from django.db import models
from core.models import BaseModel

class Organization(BaseModel):
    name = models.CharField(max_length=255, unique=True, verbose_name="Название организации")
    contact_email = models.EmailField(blank=True, null=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"
        ordering = ['name']

    def __str__(self):
        return self.name
