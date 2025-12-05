#from django.shortcuts import redirect
#from django.http import HttpResponseBadRequest
#from .models import Building 

#def add_parking_history(request):
 #   if request.method != "POST":
  #      return HttpResponseBadRequest("Invalid request")

  #  building_id = request.POST.get("building_id")
   # building = Building.objects.get(id=building_id)

    # Get info again (same as your JSON view)
   # closest = building.closestLot
  #  dist = building.distance

    # Create one combined history entry
  #  history_item = f"{building.buildingName} – {closest} – {dist} miles"

    # Save to session
 #   history = request.session.get("parking_history", [])
  #  history.append(history_item)
  #  request.session["parking_history"] = history

 #   return redirect('parking_history_list')


#from django.shortcuts import render
#from django.http import JsonResponse
#from .models import ParkingHistory
#from django.views.decorators.csrf import csrf_exempt
#from decimal import Decimal




#@csrf_exempt  
#def add_history(request):
 #   if request.method == "POST":
 #       building_name = request.POST.get("building_name")
  #      closest_lot = request.POST.get("closest_lot")
  #      distance = request.POST.get("distance")

   #     if distance:
   #         distance = Decimal(distance)


  #      user = request.user if request.user.is_authenticated else None

  #      history = ParkingHistory.objects.create(
   #         user=user,
   #         building_name=building_name,
   #         closest_lot=closest_lot,
   #         distance=distance
   #     )

  #      return JsonResponse({"status": "success"})
  #  return JsonResponse({"status": "fail"}, status=400)

#def list_history(request):
 #   if request.user.is_authenticated:
   #     history = ParkingHistory.objects.filter(user=request.user).order_by('-timestamp')
  #  else:
   #     history = ParkingHistory.objects.all().order_by('-timestamp')
   # return render(request, "parkingLotHistory/history.html", {"history": history})

from django.shortcuts import render
from django.http import JsonResponse
from .models import ParkingHistory
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal

@csrf_exempt
def add_history(request):
    if request.method == "POST":
        building_name = request.POST.get("building_name")
        closest_lot = request.POST.get("closest_lot")
        distance = request.POST.get("distance")
        if distance:
            distance = Decimal(distance)
        user = request.user if request.user.is_authenticated else None
        ParkingHistory.objects.create(
            user=user,
            building_name=building_name,
            closest_lot=closest_lot,
            distance=distance
        )
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "fail"}, status=400)

def list_history(request):
    if request.user.is_authenticated:
        history = ParkingHistory.objects.filter(user=request.user).order_by('-timestamp')
    else:
        history = ParkingHistory.objects.all().order_by('-timestamp')
    return render(request, "parkingLotHistory/history.html", {"history": history})


