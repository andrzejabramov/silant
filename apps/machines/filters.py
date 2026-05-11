import django_filters
from .models import Machine

class MachineFilter(django_filters.FilterSet):
    technique_model = django_filters.CharFilter(field_name='technique_model__name', lookup_expr='icontains', label='Модель техники')
    engine_model = django_filters.CharFilter(field_name='engine_model__name', lookup_expr='icontains', label='Модель двигателя')
    transmission_model = django_filters.CharFilter(field_name='transmission_model__name', lookup_expr='icontains', label='Модель трансмиссии')
    driving_axle_model = django_filters.CharFilter(field_name='driving_axle_model__name', lookup_expr='icontains', label='Модель ведущего моста')
    steerable_axle_model = django_filters.CharFilter(field_name='steerable_axle_model__name', lookup_expr='icontains', label='Модель управляемого моста')

    class Meta:
        model = Machine
        fields = ['technique_model', 'engine_model', 'transmission_model', 'driving_axle_model', 'steerable_axle_model']