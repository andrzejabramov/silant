from django import forms
from .models import Machine

class MachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = [
            'serial_number', 'technique_model', 'engine_model', 'engine_serial',
            'transmission_model', 'transmission_serial', 'driving_axle_model', 'driving_axle_serial',
            'steerable_axle_model', 'steerable_axle_serial', 'supply_contract_number', 'supply_contract_date',
            'shipment_date', 'recipient', 'operation_address', 'equipment_options', 'client', 'service_company'
        ]
        widgets = {
            'supply_contract_date': forms.DateInput(attrs={'type': 'date'}),
            'shipment_date': forms.DateInput(attrs={'type': 'date'}),
            'operation_address': forms.Textarea(attrs={'rows': 3}),
            'equipment_options': forms.Textarea(attrs={'rows': 3}),
        }