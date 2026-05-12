from django import forms
from .models import Maintenance

class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = ['maintenance_type', 'maintenance_date', 'operating_hours', 'work_order_number', 'work_order_date', 'service_company']
        widgets = {
            'maintenance_date': forms.DateInput(attrs={'type': 'date'}),
            'work_order_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Делаем поля интуитивно понятными
        self.fields['maintenance_type'].label = 'Вид ТО'
        self.fields['maintenance_date'].label = 'Дата проведения'
        self.fields['operating_hours'].label = 'Наработка, м/час'
        self.fields['work_order_number'].label = '№ заказ-наряда'
        self.fields['work_order_date'].label = 'Дата заказ-наряда'
        self.fields['service_company'].label = 'Сервисная компания'