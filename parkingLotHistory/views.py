from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
from .models import ParkingHistory
from django.contrib.auth.decorators import login_required

 #Temporary in-memory history list
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


