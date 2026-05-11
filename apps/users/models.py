from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    ROLE_CLIENT = 'client'
    ROLE_SERVICE = 'service'
    ROLE_MANAGER = 'manager'
    ROLE_CHOICES = [
        (ROLE_CLIENT, 'Клиент'),
        (ROLE_SERVICE, 'Сервисная организация'),
        (ROLE_MANAGER, 'Менеджер'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="Пользователь")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, verbose_name="Роль")
    organization = models.ForeignKey(
        'organizations.Organization', on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name="Привязанная организация"
    )

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

    def has_role(self, *roles):
        return self.role in roles
