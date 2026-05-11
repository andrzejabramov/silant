from django_filters.views import FilterView
from django.views import View
from django.views.generic import DetailView
from django.shortcuts import render
from .models import Machine
from .filters import MachineFilter
from core.mixins import MachineAccessMixin

class MachineListView(MachineAccessMixin, FilterView):
    model = Machine
    filterset_class = MachineFilter
    template_name = 'machines/machine_list.html'
    context_object_name = 'machines'
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Машины'
        return context


class GuestSearchView(View):
    def get(self, request):
        serial = request.GET.get('serial_number', '').strip()
        machine = None
        error = None

        if serial:
            machine = Machine.objects.filter(serial_number__iexact=serial, is_deleted=False).first()
            if not machine:
                error = "Данных о машине с таким заводским номером нет в системе."

        return render(request, 'machines/partials/_guest_search_result.html', {
            'machine': machine,
            'error': error
        })


class MachineDetailView(DetailView):
    model = Machine
    template_name = 'machines/machine_detail.html'
    context_object_name = 'machine'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['maintenance_list'] = self.object.maintenance_records.all().order_by('-maintenance_date')
        context['claims_list'] = self.object.claims.all().order_by('-failure_date')
        context['title'] = f"Машина {self.object.serial_number}"
        return context