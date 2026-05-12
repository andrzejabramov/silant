from django import forms
from .models import Claim

class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ['failure_date', 'operating_hours', 'failure_node', 'failure_description', 'restoration_method', 'spare_parts_used', 'restoration_date', 'status', 'service_company']
        widgets = {
            'failure_date': forms.DateInput(attrs={'type': 'date'}),
            'restoration_date': forms.DateInput(attrs={'type': 'date'}),
            'failure_description': forms.Textarea(attrs={'rows': 4}),
            'spare_parts_used': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['failure_date'].label = 'Дата отказа'
        self.fields['operating_hours'].label = 'Наработка, м/час'
        self.fields['failure_node'].label = 'Узел отказа'
        self.fields['failure_description'].label = 'Описание отказа'
        self.fields['restoration_method'].label = 'Способ восстановления'
        self.fields['spare_parts_used'].label = 'Запасные части'
        self.fields['restoration_date'].label = 'Дата восстановления'
        self.fields['status'].label = 'Статус'
        self.fields['service_company'].label = 'Сервисная компания'