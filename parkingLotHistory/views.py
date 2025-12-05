
from django.shortcuts import render

# Temporary in-memory history
parking_history = []

def parking_history(request):
    # Pass the list to the template
    return render(request, 'parkingLotHistory/history.html', {'history': parking_history})
