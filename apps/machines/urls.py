from django.urls import path
from . import views

urlpatterns = [
    path('', views.MachineListView.as_view(), name='machine_list'),
    path('search/', views.GuestSearchView.as_view(), name='guest_search'),
    path('<uuid:pk>/', views.MachineDetailView.as_view(), name='machine_detail'),
]

app_name = 'machines'