from django.shortcuts import render, redirect, get_object_or_404
from parkinglotlocater.models import Building
from .forms import ClassInputForm
from .models import ClassInput

# Create your views here.

def get_closest_parking(location: str) -> str:
    """
    Attempts to find closest parking lot for the given class location.
    Matches based on buildingName in the Building model.
    """
    try:
        building = Building.objects.get(buildingName__iexact=location.strip())
        return building.closestLot
    except Building.DoesNotExist:
        return "Unknown"

def schedule(request):
    if request.method == "POST":
        form = ClassInputForm(request.POST)
        if form.is_valid():
            class_input = form.save(commit=False)
            class_input.full_clean()  # calls start<end validation
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

def delete_class(request, pk):
    class_instance = get_object_or_404(ClassInput, pk=pk)
    class_instance.delete()
    return redirect("schedule")
