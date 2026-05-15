# apps/references/urls.py
from django.urls import path
from .views import ReferenceModalView

app_name = "references"

urlpatterns = [
    # Универсальный путь: /references/ajax/engine/<uuid>/
    path(
        "ajax/<str:model_name>/<uuid:pk>/",
        ReferenceModalView.as_view(),
        name="reference_modal_ajax",
    ),
]
