from datetime import date
from decimal import Decimal
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from farmops.models import Activity, Crop, Expense, Farm, Harvest


class Command(BaseCommand):
    help = "Create demo farmer data for academic evaluation."

    def handle(self, *args, **options):
        user, _ = User.objects.get_or_create(username="demo_farmer", defaults={"email": "demo@example.com", "first_name": "Demo"})
        user.set_password("DemoPass123")
        user.save()
        farm, _ = Farm.objects.get_or_create(
            owner=user,
            farm_name="Green Valley Farm",
            defaults={
                "owner_name": "Demo Farmer",
                "farm_type": "mixed",
                "address": "Village Main Road",
                "district": "Mandya",
                "state": "Karnataka",
                "length": Decimal("10.00"),
                "width": Decimal("8.00"),
                "total_area": Decimal("5.50"),
                "soil_type": "Loamy",
                "irrigation_type": "Drip",
                "water_source": "Borewell",
                "water_availability": "Seasonal",
            },
        )
        crop, _ = Crop.objects.get_or_create(
            farm=farm,
            crop_code="PADDY-01",
            defaults={
                "crop_registration_number": "CR-2026-001",
                "crop_name": "Paddy",
                "crop_variety": "Sona Masuri",
                "crop_category": "Cereal",
                "season": "kharif",
                "sowing_date": date(2026, 6, 1),
                "sowing_method": "Transplanting",
                "seed_spacing": "20 cm x 15 cm",
                "crop_status": "growing",
            },
        )
        Activity.objects.get_or_create(crop=crop, activity_name="First irrigation", defaults={"activity_type": "irrigation", "activity_date": date(2026, 6, 4), "activity_status": "completed", "performed_date": date(2026, 6, 4)})
        Expense.objects.get_or_create(crop=crop, expense_category="seed", expense_date=date(2026, 6, 1), defaults={"quantity": Decimal("25.00"), "total_expense_amount": Decimal("1250.00"), "payment_details": "cash"})
        Harvest.objects.get_or_create(crop=crop, harvest_date=date(2026, 10, 15), defaults={"harvest_start_date": date(2026, 10, 12), "harvest_end_date": date(2026, 10, 15), "harvest_season": "Kharif", "harvested_quantity": Decimal("1000.00"), "expected_yield": Decimal("900.00"), "actual_yield": Decimal("1000.00"), "is_sold": True, "selling_price": Decimal("25.00"), "total_income": Decimal("25000.00"), "buyer_details": "Demo Buyer", "selling_date": date(2026, 10, 20)})
        self.stdout.write(self.style.SUCCESS("Demo data created. Login: demo_farmer / DemoPass123"))
