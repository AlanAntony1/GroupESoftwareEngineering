from django.http import JsonResponse
from .models import Building  # or your building model

def add_to_history_ajax(request):
    if request.method == "POST":
        building_id = request.POST.get('building_id')
        try:
            building = Building.objects.get(id=building_id)
        except Building.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Building not found"})

        # Get current session history or initialize
        history = request.session.get('parking_history', [])
        if building.buildingName not in history:
            history.append(building.buildingName)
            request.session['parking_history'] = history

        return JsonResponse({"status": "success", "history": history})
    return JsonResponse({"status": "error", "message": "Invalid request"})
