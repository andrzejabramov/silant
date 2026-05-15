from django.urls import path
from . import views

urlpatterns = [
    path(
        "ajax/<uuid:pk>/", views.MachineModalView.as_view(), name="machine_modal_ajax"
    ),
    path("", views.MachineListView.as_view(), name="machine_list"),
    path("add/", views.add_machine, name="add_machine"),
    path("search/", views.GuestSearchView.as_view(), name="guest_search"),
    path("<uuid:pk>/", views.MachineDetailView.as_view(), name="machine_detail"),
    path(
        "<uuid:machine_pk>/maintenance/add/",
        views.add_maintenance,
        name="add_maintenance",
    ),
    path("<uuid:machine_pk>/claim/add/", views.add_claim, name="add_claim"),
]

app_name = "machines"
