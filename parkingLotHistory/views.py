# views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
from .models import ParkingHistory
from django.contrib.auth.decorators import login_required


@login_required
def parking_history(request):
    # Get history for the logged-in user
    history = ParkingHistory.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'parkingLotHistory/history.html', {'history': history})

@csrf_exempt
@login_required
def add_history(request):
    if request.method == 'POST':
        building_name = request.POST.get('building_name')
        if building_name:
            ParkingHistory.objects.create(user=request.user, building_name=building_name)
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'}, status=400)
