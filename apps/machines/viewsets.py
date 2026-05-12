from rest_framework import viewsets, permissions
from .models import Machine
from .serializers import MachineSerializer
from core.mixins import MachineAccessMixin

class MachineViewSet(MachineAccessMixin, viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Применяем ту же логику фильтрации, что и в веб-интерфейсе
        qs = super().get_queryset()
        return qs.order_by('-shipment_date')