from django.contrib import admin
from .models import Activity, Crop, Expense, Farm, Harvest

@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ("farm_name", "owner", "district", "state", "total_area", "farm_type")
    search_fields = ("farm_name", "owner_name", "district", "state")
    list_filter = ("farm_type", "state", "soil_type")

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ("crop_name", "crop_variety", "farm", "season", "sowing_date", "crop_status")
    search_fields = ("crop_name", "crop_variety", "crop_code")
    list_filter = ("season", "crop_status")

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("activity_name", "crop", "activity_type", "activity_date", "activity_status")
    list_filter = ("activity_type", "activity_status")

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("crop", "expense_category", "expense_date", "total_expense_amount", "payment_details")
    list_filter = ("expense_category", "payment_details")

@admin.register(Harvest)
class HarvestAdmin(admin.ModelAdmin):
    list_display = ("crop", "harvest_date", "harvested_quantity", "unit_of_measurement", "total_income", "is_sold")
    list_filter = ("is_sold", "yield_quality", "harvest_season")
