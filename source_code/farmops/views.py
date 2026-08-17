from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q, Sum
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView
from .forms import ActivityForm, CropForm, ExpenseForm, FarmForm, FarmerRegistrationForm, HarvestForm
from .models import Activity, Crop, Expense, Farm, Harvest


class RegisterView(CreateView):
    form_class = FarmerRegistrationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "Account created successfully.")
        return response


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "farmops/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        crops = Crop.objects.filter(farm__owner=user)
        expenses = Expense.objects.filter(crop__farm__owner=user)
        harvests = Harvest.objects.filter(crop__farm__owner=user)
        expense_total = expenses.aggregate(total=Sum("total_expense_amount"))["total"] or Decimal("0.00")
        income_total = harvests.aggregate(total=Sum("total_income"))["total"] or Decimal("0.00")
        context.update({
            "farm_count": Farm.objects.filter(owner=user).count(),
            "crop_count": crops.count(),
            "activity_count": Activity.objects.filter(crop__farm__owner=user).count(),
            "expense_total": expense_total,
            "income_total": income_total,
            "profit_total": income_total - expense_total,
            "recent_crops": crops.select_related("farm")[:5],
            "recent_harvests": harvests.select_related("crop")[:5],
            "status_rows": crops.values("crop_status").annotate(total=Count("id")).order_by("crop_status"),
        })
        return context


class OwnedQuerysetMixin(LoginRequiredMixin):
    owner_path = "owner"

    def get_queryset(self):
        queryset = super().get_queryset()
        lookup = {self.owner_path: self.request.user}
        query = self.request.GET.get("q", "").strip()
        queryset = queryset.filter(**lookup)
        return self.apply_search(queryset, query)

    def apply_search(self, queryset, query):
        return queryset

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.model in {Crop, Activity, Expense, Harvest}:
            kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        if self.model is Farm and not form.instance.owner_id:
            form.instance.owner = self.request.user
        messages.success(self.request, f"{self.model._meta.verbose_name.title()} saved successfully.")
        return super().form_valid(form)


class FarmListView(OwnedQuerysetMixin, ListView):
    model = Farm
    paginate_by = 10
    template_name = "farmops/list.html"
    owner_path = "owner"

    def apply_search(self, queryset, query):
        if query:
            queryset = queryset.filter(Q(farm_name__icontains=query) | Q(district__icontains=query) | Q(state__icontains=query))
        return queryset


class FarmCreateView(OwnedQuerysetMixin, CreateView):
    model = Farm
    form_class = FarmForm
    template_name = "farmops/form.html"


class FarmUpdateView(OwnedQuerysetMixin, UpdateView):
    model = Farm
    form_class = FarmForm
    template_name = "farmops/form.html"


class FarmDetailView(OwnedQuerysetMixin, DetailView):
    model = Farm
    template_name = "farmops/detail.html"


class FarmDeleteView(OwnedQuerysetMixin, DeleteView):
    model = Farm
    success_url = reverse_lazy("farm-list")
    template_name = "farmops/confirm_delete.html"


class CropListView(OwnedQuerysetMixin, ListView):
    model = Crop
    paginate_by = 10
    template_name = "farmops/list.html"
    owner_path = "farm__owner"

    def apply_search(self, queryset, query):
        queryset = queryset.select_related("farm")
        if query:
            queryset = queryset.filter(Q(crop_name__icontains=query) | Q(crop_variety__icontains=query) | Q(crop_code__icontains=query))
        return queryset


class CropCreateView(OwnedQuerysetMixin, CreateView):
    model = Crop
    form_class = CropForm
    template_name = "farmops/form.html"


class CropUpdateView(OwnedQuerysetMixin, UpdateView):
    model = Crop
    form_class = CropForm
    template_name = "farmops/form.html"
    owner_path = "farm__owner"


class CropDetailView(OwnedQuerysetMixin, DetailView):
    model = Crop
    template_name = "farmops/detail.html"
    owner_path = "farm__owner"


class CropDeleteView(OwnedQuerysetMixin, DeleteView):
    model = Crop
    success_url = reverse_lazy("crop-list")
    template_name = "farmops/confirm_delete.html"
    owner_path = "farm__owner"


class ActivityListView(OwnedQuerysetMixin, ListView):
    model = Activity
    paginate_by = 10
    template_name = "farmops/list.html"
    owner_path = "crop__farm__owner"

    def apply_search(self, queryset, query):
        queryset = queryset.select_related("crop", "crop__farm")
        if query:
            queryset = queryset.filter(Q(activity_name__icontains=query) | Q(activity_type__icontains=query))
        return queryset


class ActivityCreateView(OwnedQuerysetMixin, CreateView):
    model = Activity
    form_class = ActivityForm
    template_name = "farmops/form.html"


class ActivityUpdateView(OwnedQuerysetMixin, UpdateView):
    model = Activity
    form_class = ActivityForm
    template_name = "farmops/form.html"
    owner_path = "crop__farm__owner"


class ActivityDetailView(OwnedQuerysetMixin, DetailView):
    model = Activity
    template_name = "farmops/detail.html"
    owner_path = "crop__farm__owner"


class ActivityDeleteView(OwnedQuerysetMixin, DeleteView):
    model = Activity
    success_url = reverse_lazy("activity-list")
    template_name = "farmops/confirm_delete.html"
    owner_path = "crop__farm__owner"


class ExpenseListView(OwnedQuerysetMixin, ListView):
    model = Expense
    paginate_by = 10
    template_name = "farmops/list.html"
    owner_path = "crop__farm__owner"

    def apply_search(self, queryset, query):
        queryset = queryset.select_related("crop", "crop__farm")
        if query:
            queryset = queryset.filter(Q(expense_category__icontains=query) | Q(payment_details__icontains=query))
        return queryset


class ExpenseCreateView(OwnedQuerysetMixin, CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = "farmops/form.html"


class ExpenseUpdateView(OwnedQuerysetMixin, UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = "farmops/form.html"
    owner_path = "crop__farm__owner"


class ExpenseDetailView(OwnedQuerysetMixin, DetailView):
    model = Expense
    template_name = "farmops/detail.html"
    owner_path = "crop__farm__owner"


class ExpenseDeleteView(OwnedQuerysetMixin, DeleteView):
    model = Expense
    success_url = reverse_lazy("expense-list")
    template_name = "farmops/confirm_delete.html"
    owner_path = "crop__farm__owner"


class HarvestListView(OwnedQuerysetMixin, ListView):
    model = Harvest
    paginate_by = 10
    template_name = "farmops/list.html"
    owner_path = "crop__farm__owner"

    def apply_search(self, queryset, query):
        queryset = queryset.select_related("crop", "crop__farm")
        if query:
            queryset = queryset.filter(Q(crop__crop_name__icontains=query) | Q(harvest_season__icontains=query) | Q(buyer_details__icontains=query))
        return queryset


class HarvestCreateView(OwnedQuerysetMixin, CreateView):
    model = Harvest
    form_class = HarvestForm
    template_name = "farmops/form.html"


class HarvestUpdateView(OwnedQuerysetMixin, UpdateView):
    model = Harvest
    form_class = HarvestForm
    template_name = "farmops/form.html"
    owner_path = "crop__farm__owner"


class HarvestDetailView(OwnedQuerysetMixin, DetailView):
    model = Harvest
    template_name = "farmops/detail.html"
    owner_path = "crop__farm__owner"


class HarvestDeleteView(OwnedQuerysetMixin, DeleteView):
    model = Harvest
    success_url = reverse_lazy("harvest-list")
    template_name = "farmops/confirm_delete.html"
    owner_path = "crop__farm__owner"


class ReportsView(LoginRequiredMixin, TemplateView):
    template_name = "farmops/reports.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["expense_by_category"] = Expense.objects.filter(crop__farm__owner=user).values("expense_category").annotate(total=Sum("total_expense_amount"))
        context["harvest_by_crop"] = Harvest.objects.filter(crop__farm__owner=user).values("crop__crop_name").annotate(quantity=Sum("harvested_quantity"), income=Sum("total_income"))
        context["crop_status"] = Crop.objects.filter(farm__owner=user).values("crop_status").annotate(total=Count("id"))
        return context
