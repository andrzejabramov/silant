from django_filters.views import FilterView
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