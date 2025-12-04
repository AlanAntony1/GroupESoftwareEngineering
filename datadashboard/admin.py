# datadashboard/admin.py
from django.contrib import admin
from .models import DataReport

@admin.register(DataReport)
class DataReportAdmin(admin.ModelAdmin):
    list_display = ("report_name", "start_date", "end_date", "format", "rows_count", "created_at")
    list_filter = ("format", "created_at")
    search_fields = ("report_name", "lot_id")
