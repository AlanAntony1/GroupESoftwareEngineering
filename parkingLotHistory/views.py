from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ParkingHistory, HousingHistory
import datetime

def parking_history(request):
    history = ParkingHistory.objects.order_by('-timestamp')  # get all records
    return render(request, 'parkingLotHistory/history.html', {'history': history})

def housing_history(request):
    history = HousingHistory.objects.order_by('-timestamp')
    return render(request, 'housinglotlocater/history.html', {'history': history})

@csrf_exempt
def add_parking_history(request):
    if request.method == 'POST':
        building_name = request.POST.get('building_name')
        if building_name:
            ParkingHistory.objects.create(lot_name=building_name)
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'}, status=400)

@csrf_exempt
def add_housing_history(request):
    if request.method == 'POST':
        building_name = request.POST.get('building_name')
        if building_name:
            HousingHistory.objects.create(building_name=building_name)
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


