# apps/users/urls.py
from django.urls import path
from . import views

# 🔹 ЭТО КРИТИЧНО: задает пространство имен для {% url 'users:...' %}
app_name = "users"

urlpatterns = [
    # Путь к профилю (если вьюхи еще нет — создай заглушку, см. Шаг 3)
    # path("profile/", views.profile_view, name="profile"),
]
