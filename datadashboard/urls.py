# datadashboard/urls.py
# ------------------------------------------------------------
# Purpose:
#   Define the URL patterns (routes) for the Data Dashboard app.
#   These patterns are included from OUParking/urls.py at path("dashboard/", ...).
#
# How it resolves:
#   Visiting /dashboard/           → calls views.home (HTML page)
#   Visiting /dashboard/data.json  → calls views.data_json (JSON API)
#
# What to change / extend:
#   - To add a new endpoint (e.g., /dashboard/peak-hours/), add another path(...)
#     and implement the corresponding view in datadashboard/views.py.
#   - Keep app_name="datadashboard" so reverse() / {% url %} can use the
#     "datadashboard:<name>" namespace (tests rely on names like "dashboard-home"
#     and "dashboard-data").
# ------------------------------------------------------------

from django.urls import path
from . import views

# Namespace for reversing URLs: reverse("datadashboard:dashboard-home")
app_name = "datadashboard"

urlpatterns = [
    # /dashboard/
    # Name used in templates/tests:
    #   reverse("datadashboard:dashboard-home")
    #   {% url "datadashboard:dashboard-home" %}
    path("", views.home, name="dashboard-home"),

    # /dashboard/data.json
    # JSON endpoint that returns a TOP-LEVEL LIST (tests expect a list, not {"rows": ...}).
    # Name used in tests:
    #   reverse("datadashboard:dashboard-data")
    path("data.json", views.data_json, name="dashboard-data"),

    # EXAMPLES (uncomment/implement in views.py if you add these):
    # path("peak-hours/<str:lot_code>/", views.peak_hours, name="dashboard-peak-hours")
    # path("export/<str:fmt>/", views.export_stats, name="dashboard-export")
]





