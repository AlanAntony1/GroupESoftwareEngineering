# views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime

# Temporary in-memory history list
parking_history_list = []

def parking_history(request):
    """
    Display the parking history page
    """
    return render(request, 'parkingLotHistory/history.html', {
        'history': parking_history_list
    })

@csrf_exempt
def add_history(request):
    """
    Receive POST request with building name and record it.
    """
    if request.method == 'POST':
        building_name = request.POST.get('building_name')

        if building_name:
            parking_history_list.append({
                'building_name': building_name,
                'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'fail'}, status=400)
