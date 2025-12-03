from django.shortcuts import render, redirect
from .forms import ClassInputForm
from .models import ClassInput

# Create your views here.

def get_closest_parking(location: str) -> str:
    """
    Use logic from ParkingLotLocator
    """
    return "Unknown"

def schedule(request):
    if request.method == "POST":
        form = ClassInputForm(request.POST)
        if form.is_valid():
            class_input = form.save(commit=False)
            class_input.full_clean()  # calls your start<end validation
            class_input.save()
            return redirect("schedule")  # avoid resubmission on refresh
    else:
        form = ClassInputForm()

    classes = ClassInput.objects.all()

    # attach closest parking dynamically (not stored in db)
    for c in classes:
        c.closest_parking = get_closest_parking(c.location)

    return render(request, "scheduleInput/schedule.html", {
        "form": form,
        "classes": classes,
    })
