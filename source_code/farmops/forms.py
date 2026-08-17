from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Activity, Crop, Expense, Farm, Harvest


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs.setdefault("class", "form-check-input")
            else:
                widget.attrs.setdefault("class", "form-control")


class FarmerRegistrationForm(BootstrapFormMixin, UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150, required=False)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]


class FarmForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Farm
        exclude = ["owner", "created_at", "updated_at"]
        widgets = {"address": forms.Textarea(attrs={"rows": 3}), "soil_test_result": forms.Textarea(attrs={"rows": 3})}


class CropForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Crop
        exclude = ["created_at", "updated_at"]
        widgets = {"sowing_date": forms.DateInput(attrs={"type": "date"}), "notes": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["farm"].queryset = Farm.objects.filter(owner=user)


class ActivityForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Activity
        exclude = ["created_at", "updated_at"]
        widgets = {
            "activity_date": forms.DateInput(attrs={"type": "date"}),
            "performed_date": forms.DateInput(attrs={"type": "date"}),
            "remarks": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["crop"].queryset = Crop.objects.filter(farm__owner=user)


class ExpenseForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Expense
        exclude = ["created_at", "updated_at"]
        widgets = {"expense_date": forms.DateInput(attrs={"type": "date"}), "notes": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["crop"].queryset = Crop.objects.filter(farm__owner=user)


class HarvestForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Harvest
        exclude = ["created_at", "updated_at"]
        widgets = {
            "harvest_date": forms.DateInput(attrs={"type": "date"}),
            "harvest_start_date": forms.DateInput(attrs={"type": "date"}),
            "harvest_end_date": forms.DateInput(attrs={"type": "date"}),
            "storage_date": forms.DateInput(attrs={"type": "date"}),
            "selling_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["crop"].queryset = Crop.objects.filter(farm__owner=user)
