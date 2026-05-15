# apps/organizations/models.py
from django.db import models
from core.models import BaseModel


class Organization(BaseModel):
    name = models.CharField(
        max_length=255, unique=True, verbose_name="Название организации", db_index=True
    )
    contact_email = models.EmailField(blank=True, null=True, verbose_name="Email")
    phone = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Телефон"
    )

    # 🔹 Флаги ролей (независимые: организация может иметь любую комбинацию)
    # Все с default=False → существующие записи не сломаются
    is_buyer = models.BooleanField(
        "Покупатель",
        default=False,
        help_text="Фигурирует в поле 'Покупатель' в данных завода",
    )
    is_client = models.BooleanField(
        "Клиент (грузополучатель)",
        default=False,
        help_text="Конечный потребитель / эксплуатант техники",
    )
    is_service_company = models.BooleanField(
        "Сервисная компания", default=False, help_text="Выполняет ТО и ремонтные работы"
    )

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_role_display(self):
        """Вспомогательный метод: возвращает строку с ролями для отображения"""
        roles = []
        if self.is_buyer:
            roles.append("Покупатель")
        if self.is_client:
            roles.append("Клиент")
        if self.is_service_company:
            roles.append("Сервис")
        return ", ".join(roles) if roles else "—"
