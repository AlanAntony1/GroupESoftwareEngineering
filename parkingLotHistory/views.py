

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime

# Temporary in-memory history lists
parking_history_list = []
housing_history_list = []

def parking_history(request):
    """
    Display the temporary parking history page.
    """
    return render(request, 'parkingLotHistory/history.html', {
        'history': parking_history_list
    })

def housing_history(request):
    """
    Display the temporary housing history page.
    """
    return render(request, 'housinglotlocater/history.html', {
        'history': housing_history_list
    })

@csrf_exempt
def add_parking_history(request):
    """
    Add a building selection to the temporary parking history.
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

@csrf_exempt
def add_housing_history(request):
    """
    Add a building selection to the temporary housing history.
    """
    if request.method == 'POST':
        building_name = request.POST.get('building_name')

        if building_name:
            housing_history_list.append({
                'building_name': building_name,
                'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'fail'}, status=400)


#from django.shortcuts import render
#from django.contrib.auth.decorators import login_required
#from parkingLotHistory.models import ParkingHistory   # absolute import
#from django.http import JsonResponse


#@login_required
#def parking_history(request):
    # Get history for the logged-in user
 #   history = ParkingHistory.objects.filter(user=request.user).order_by('-timestamp')
  #  return render(request, 'parkingLotHistory/history.html', {'history': history})

#@login_required
#def add_history(request):
 #   if request.method == 'POST':
  #      building_name = request.POST.get('building_name', 'Unknown')
  #      ParkingHistory.objects.create(user=request.user, building_name=building_name)
   #     return JsonResponse({'status': 'ok'})


