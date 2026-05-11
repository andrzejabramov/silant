from django.urls import path
from . import views

urlpatterns = [
    path('', views.MachineListView.as_view(), name='machine_list'),
]