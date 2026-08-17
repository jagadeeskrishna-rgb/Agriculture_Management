from datetime import date
from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Crop, Expense, Farm, Harvest


class AgricultureWorkflowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="farmer", password="StrongPass123", email="farmer@example.com")
        self.other = User.objects.create_user(username="other", password="StrongPass123")
        self.farm = Farm.objects.create(
            owner=self.user,
            farm_name="Green Valley",
            owner_name="Demo Farmer",
            farm_type="mixed",
            address="Village Road",
            district="Mandya",
            state="Karnataka",
            length=Decimal("10.00"),
            width=Decimal("8.00"),
            total_area=Decimal("5.50"),
            soil_type="Loamy",
            irrigation_type="Drip",
            water_source="Borewell",
            water_availability="Seasonal",
        )
        self.crop = Crop.objects.create(
            farm=self.farm,
            crop_registration_number="CR-001",
            crop_code="PADDY-01",
            crop_name="Paddy",
            crop_variety="Sona Masuri",
            crop_category="Cereal",
            season="kharif",
            sowing_date=date(2026, 6, 1),
            sowing_method="Transplanting",
            crop_status="growing",
        )

    def test_profit_or_loss_uses_crop_expenses(self):
        Expense.objects.create(
            crop=self.crop,
            expense_date=date(2026, 6, 10),
            expense_category="seed",
            total_expense_amount=Decimal("1200.00"),
        )
        harvest = Harvest.objects.create(
            crop=self.crop,
            harvest_date=date(2026, 10, 15),
            harvest_start_date=date(2026, 10, 12),
            harvest_end_date=date(2026, 10, 15),
            harvest_season="Kharif",
            harvested_quantity=Decimal("1000.00"),
            expected_yield=Decimal("900.00"),
            actual_yield=Decimal("1000.00"),
            total_income=Decimal("25000.00"),
            is_sold=True,
        )
        self.assertEqual(harvest.yield_difference, Decimal("100.00"))
        self.assertEqual(harvest.profit_or_loss, Decimal("23800.00"))

    def test_authenticated_user_sees_dashboard(self):
        self.client.login(username="farmer", password="StrongPass123")
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Green Valley")

    def test_farmer_cannot_view_other_farm(self):
        other_farm = Farm.objects.create(
            owner=self.other,
            farm_name="Hidden Farm",
            owner_name="Other Farmer",
            farm_type="organic",
            address="Other",
            district="Other",
            state="Other",
            length=Decimal("1.00"),
            width=Decimal("1.00"),
            total_area=Decimal("1.00"),
            soil_type="Clay",
            irrigation_type="Canal",
            water_source="Canal",
            water_availability="Regular",
        )
        self.client.login(username="farmer", password="StrongPass123")
        response = self.client.get(reverse("farm-detail", args=[other_farm.pk]))
        self.assertEqual(response.status_code, 404)
