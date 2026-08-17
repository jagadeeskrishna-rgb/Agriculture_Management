from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Farm(TimeStampedModel):
    FARM_TYPES = [
        ("organic", "Organic"),
        ("traditional", "Traditional"),
        ("mixed", "Mixed"),
        ("greenhouse", "Greenhouse"),
    ]
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="farms")
    farm_name = models.CharField(max_length=120)
    owner_name = models.CharField(max_length=120)
    registration_number = models.CharField(max_length=60, blank=True)
    farm_type = models.CharField(max_length=20, choices=FARM_TYPES, default="mixed")
    address = models.TextField()
    district = models.CharField(max_length=80)
    state = models.CharField(max_length=80)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    measurement_unit = models.CharField(max_length=20, default="acre")
    length = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))])
    width = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))])
    total_area = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    soil_type = models.CharField(max_length=80)
    soil_test_result = models.TextField(blank=True)
    irrigation_type = models.CharField(max_length=80)
    water_source = models.CharField(max_length=80)
    water_availability = models.CharField(max_length=80)
    irrigation_schedule = models.CharField(max_length=120, blank=True)
    water_usage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ["farm_name"]
        constraints = [
            models.UniqueConstraint(fields=["owner", "farm_name"], name="unique_farm_name_per_owner")
        ]

    def __str__(self):
        return self.farm_name

    def get_absolute_url(self):
        return reverse("farm-detail", kwargs={"pk": self.pk})


class Crop(TimeStampedModel):
    STATUS_CHOICES = [
        ("planned", "Planned"),
        ("sown", "Sown"),
        ("growing", "Growing"),
        ("ready", "Ready for Harvest"),
        ("harvested", "Harvested"),
        ("cancelled", "Cancelled"),
    ]
    SEASONS = [
        ("kharif", "Kharif"),
        ("rabi", "Rabi"),
        ("zaid", "Zaid"),
        ("annual", "Annual"),
    ]
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name="crops")
    crop_registration_number = models.CharField(max_length=60)
    crop_code = models.CharField(max_length=30)
    crop_name = models.CharField(max_length=100)
    crop_variety = models.CharField(max_length=100)
    crop_category = models.CharField(max_length=80)
    season = models.CharField(max_length=20, choices=SEASONS)
    sowing_date = models.DateField()
    sowing_method = models.CharField(max_length=80)
    seed_spacing = models.CharField(max_length=80, blank=True)
    crop_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="planned")
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-sowing_date", "crop_name"]
        constraints = [
            models.UniqueConstraint(fields=["farm", "crop_code"], name="unique_crop_code_per_farm")
        ]

    def __str__(self):
        return f"{self.crop_name} - {self.crop_variety}"

    def get_absolute_url(self):
        return reverse("crop-detail", kwargs={"pk": self.pk})


class Activity(TimeStampedModel):
    TYPE_CHOICES = [
        ("sowing", "Sowing"),
        ("irrigation", "Irrigation"),
        ("fertilization", "Fertilization"),
        ("pest_control", "Pest Control"),
        ("spraying", "Pesticide Spraying"),
        ("weeding", "Weeding"),
        ("other", "Other"),
    ]
    STATUS_CHOICES = [
        ("planned", "Planned"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name="activities")
    activity_name = models.CharField(max_length=120)
    activity_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    activity_date = models.DateField()
    performed_date = models.DateField(null=True, blank=True)
    activity_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="planned")
    remarks = models.TextField(blank=True)

    class Meta:
        ordering = ["activity_date"]

    def __str__(self):
        return self.activity_name

    def get_absolute_url(self):
        return reverse("activity-detail", kwargs={"pk": self.pk})


class Expense(TimeStampedModel):
    CATEGORY_CHOICES = [
        ("seed", "Seed"),
        ("fertilizer", "Fertilizer"),
        ("pesticide", "Pesticide"),
        ("labour", "Labour"),
        ("machinery", "Machinery"),
        ("irrigation", "Irrigation"),
        ("transport", "Transportation"),
        ("other", "Other"),
    ]
    PAYMENT_CHOICES = [("cash", "Cash"), ("upi", "UPI"), ("bank", "Bank"), ("credit", "Credit")]
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name="expenses")
    expense_date = models.DateField()
    expense_period = models.CharField(max_length=80, blank=True)
    expense_category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    labour_details = models.CharField(max_length=160, blank=True)
    machinery_usage_duration = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    rental_or_maintenance_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    water_usage_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    distance_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_details = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default="cash")
    total_expense_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))])
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-expense_date"]

    def __str__(self):
        return f"{self.crop.crop_name} - {self.get_expense_category_display()} - {self.total_expense_amount}"

    def get_absolute_url(self):
        return reverse("expense-detail", kwargs={"pk": self.pk})


class Harvest(TimeStampedModel):
    QUALITY_CHOICES = [("excellent", "Excellent"), ("good", "Good"), ("average", "Average"), ("poor", "Poor")]
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name="harvests")
    harvest_date = models.DateField()
    harvest_start_date = models.DateField()
    harvest_end_date = models.DateField()
    harvest_season = models.CharField(max_length=40)
    harvested_quantity = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))])
    unit_of_measurement = models.CharField(max_length=20, default="kg")
    expected_yield = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))])
    actual_yield = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))])
    yield_quality = models.CharField(max_length=20, choices=QUALITY_CHOICES, default="good")
    storage_location = models.CharField(max_length=160, blank=True)
    storage_quantity = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    storage_type = models.CharField(max_length=80, blank=True)
    storage_date = models.DateField(null=True, blank=True)
    is_sold = models.BooleanField(default=False)
    selling_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_income = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    buyer_details = models.CharField(max_length=160, blank=True)
    selling_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-harvest_date"]

    @property
    def yield_difference(self):
        return self.actual_yield - self.expected_yield

    @property
    def profit_or_loss(self):
        expense_total = self.crop.expenses.aggregate(total=models.Sum("total_expense_amount"))["total"] or Decimal("0.00")
        return self.total_income - expense_total

    def __str__(self):
        return f"{self.crop.crop_name} harvest on {self.harvest_date}"

    def get_absolute_url(self):
        return reverse("harvest-detail", kwargs={"pk": self.pk})
