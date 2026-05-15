# apps/references/views.py
from django.http import Http404
from django.views.generic import DetailView
from django.shortcuts import render

# Импортируем все модели справочников
# Проверь, что путь соответствует твоей структуре (обычно apps.references.models)
from references.models import (
    EngineModel,
    TransmissionModel,
    DrivingAxleModel,
    SteerableAxleModel,
)


class ReferenceModalView(DetailView):
    """Универсальная вьюха для показа данных справочника в модалке"""

    template_name = "references/partials/reference_modal.html"

    # Карта: имя из URL → Модель Django
    MODEL_MAP = {
        "engine": EngineModel,
        "transmission": TransmissionModel,
        "driving_axle": DrivingAxleModel,
        "steerable_axle": SteerableAxleModel,
    }

    def get_object(self, queryset=None):
        model_key = self.kwargs.get("model_name")
        pk = self.kwargs.get("pk")

        model_class = self.MODEL_MAP.get(model_key)
        if not model_class:
            raise Http404("Неизвестный тип справочника")

        try:
            return model_class.objects.get(pk=pk)
        except model_class.DoesNotExist:
            raise Http404("Запись не найдена")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Передаем имя модели для заголовка
        context["ref_type"] = self.kwargs.get("model_name")
        return context
