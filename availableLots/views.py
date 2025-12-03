from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import AvailableLots


def requestLots(request):
    """
    Public view: shows current availability to any user.
    This is read-only and NOT a critical function.
    """
    lots = AvailableLots.objects.all().order_by("lot_name")
    context = {"lots": lots}
    return render(request, "availableLots/AvailableLots.html", context)

# Security helpers: CWE-306 (Insufficient Authorization) mitigation

def _is_parking_manager(user):
    """
    Returns True if the user is allowed to modify parking data.
    For now: staff users OR members of the 'parking_manager' group.
    """
    if not user.is_authenticated:
        return False
    return user.is_staff or user.groups.filter(name="parking_manager").exists()


@login_required
@user_passes_test(_is_parking_manager)
def update_lot_availability(request, lot_id):
    """
    Critical function: updates the number of available spaces for a lot.

    CWE-306 Mitigation:
      * @login_required ensures the user is authenticated.
      * @user_passes_test(_is_parking_manager) restricts access to
        authorized roles (staff / parking managers).
      * Unauthenticated/unauthorized requests are redirected/denied.
    """
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    lot = get_object_or_404(AvailableLots, pk=lot_id)

    # Parse and validate input
    try:
        new_count = int(request.POST.get("available_spaces"))
    except (TypeError, ValueError):
        return JsonResponse(
            {"error": "available_spaces must be an integer."},
            status=400,
        )

    # Use the model’s safe update method (also validates bounds)
    try:
        lot.update_availability(new_count)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)

    # Return updated data (could be used by an admin dashboard / AJAX)
    return JsonResponse(
        {
            "lot_id": lot.lot_id,
            "lot_name": lot.lot_name,
            "available_spaces": lot.available_spaces,
            "total_spaces": lot.total_spaces,
            "status": lot.status,
        }
    )