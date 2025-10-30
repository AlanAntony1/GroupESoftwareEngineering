from django.shortcuts import render
from django.http import JsonResponse

def home(request):
    return render(request, "datadashboard/home.html", {
        "title": "OU Parking — Dashboard",
        "status": "OK",
    })

def data_json(request):
    return JsonResponse({"ok": True})
