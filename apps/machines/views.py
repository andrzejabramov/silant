from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django_filters.views import FilterView
from django.views import View
from django.views.generic import DetailView
from django.shortcuts import render, redirect, get_object_or_404
from maintenance.forms import MaintenanceForm
from maintenance.models import Maintenance
from .models import Machine
from .filters import MachineFilter
from core.mixins import MachineAccessMixin
from claims.forms import ClaimForm
from claims.models import Claim
from .forms import MachineForm


class MachineListView(MachineAccessMixin, FilterView):
    model = Machine
    filterset_class = MachineFilter
    template_name = "machines/machine_list.html"
    context_object_name = "machines"
    paginate_by = 15

    def get_template_names(self):
        # 🔹 Если запрос пришёл от HTMX, отдаём ТОЛЬКО таблицу
        if self.request.headers.get("HX-Request"):
            return ["machines/partials/_table.html"]
        # Иначе отдаём полную страницу с шапкой/подвалом
        return [self.template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Машины"
        return context


class GuestSearchView(View):
    def get(self, request):
        serial = request.GET.get("serial_number", "").strip()
        machine = None
        error = None

        if serial:
            machine = Machine.objects.filter(
                serial_number__iexact=serial, is_deleted=False
            ).first()
            if not machine:
                error = "Данных о машине с таким заводским номером нет в системе."

        return render(
            request,
            "machines/partials/_guest_search_result.html",
            {"machine": machine, "error": error},
        )


class MachineDetailView(DetailView):
    model = Machine
    template_name = "machines/machine_detail.html"
    context_object_name = "machine"

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_superuser or (
            hasattr(user, "profile") and user.profile.role == "manager"
        ):
            return qs.filter(is_deleted=False)
        if user.is_authenticated and hasattr(user, "profile"):
            profile = user.profile
            if profile.role == "client" and profile.organization:
                return qs.filter(client=profile.organization, is_deleted=False)
            if profile.role == "service" and profile.organization:
                return qs.filter(service_company=profile.organization, is_deleted=False)
        return qs.filter(client__isnull=True, is_deleted=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["maintenance_list"] = self.object.maintenance_records.all().order_by(
            "-maintenance_date"
        )
        context["claims_list"] = self.object.claims.all().order_by("-failure_date")
        context["title"] = f"Машина {self.object.serial_number}"
        return context


@login_required
def add_maintenance(request, machine_pk):
    machine = get_object_or_404(Machine, pk=machine_pk, is_deleted=False)

    # Проверка прав: только сервисная компания или менеджер
    profile = getattr(request.user, "profile", None)
    if not (
        request.user.is_superuser
        or (profile and profile.role == "service" and profile.organization)
        or (profile and profile.role == "manager")
    ):
        messages.error(request, "Нет прав для добавления ТО")
        return redirect("machines:machine_detail", pk=machine_pk)

    if request.method == "POST":
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            maintenance = form.save(commit=False)
            maintenance.machine = machine
            # Авто-привязка сервисной компании из профиля, если не выбрана
            if not maintenance.service_company and profile and profile.organization:
                maintenance.service_company = profile.organization
            maintenance.save()
            messages.success(request, "Запись о ТО добавлена")
            return redirect("machines:machine_detail", pk=machine_pk)
    else:
        form = MaintenanceForm()

    return render(
        request,
        "machines/maintenance_form.html",
        {
            "form": form,
            "machine": machine,
            "title": f"Добавить ТО | {machine.serial_number}",
        },
    )


@login_required
def add_claim(request, machine_pk):
    machine = get_object_or_404(Machine, pk=machine_pk, is_deleted=False)

    # Проверка прав: клиент, сервис или менеджер
    profile = getattr(request.user, "profile", None)
    if not (
        request.user.is_superuser
        or (
            profile
            and profile.organization
            and profile.role in ["client", "service", "manager"]
        )
    ):
        messages.error(request, "Нет прав для создания рекламации")
        return redirect("machines:machine_detail", pk=machine_pk)

    if request.method == "POST":
        form = ClaimForm(request.POST)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.machine = machine
            # Авто-привязка сервисной компании
            if not claim.service_company and profile and profile.organization:
                claim.service_company = profile.organization
            claim.save()
            messages.success(request, "Рекламация создана")
            return redirect("machines:machine_detail", pk=machine_pk)
    else:
        form = ClaimForm()

    return render(
        request,
        "machines/claim_form.html",
        {
            "form": form,
            "machine": machine,
            "title": f"Создать рекламацию | {machine.serial_number}",
        },
    )


@login_required
def add_machine(request):
    profile = getattr(request.user, "profile", None)
    is_manager = request.user.is_superuser or (profile and profile.role == "manager")

    if not is_manager:
        messages.error(request, "Доступ запрещен: функция доступна только менеджерам")
        return redirect("machines:machine_list")

    if request.method == "POST":
        form = MachineForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Машина успешно добавлена в реестр")
            return redirect("machines:machine_list")
    else:
        form = MachineForm()

    return render(
        request,
        "machines/machine_form.html",
        {"form": form, "title": "Добавить новую машину"},
    )
