from django.http import JsonResponse
from django.utils import timezone
from .models import Highlight
from HighlightButton.models import Highlight 


def togglespot(request):
    spotid = request.GET.get("spotid")
    if not spotid:
        return JsonResponse({"error": "no spotid"}, status=400)
    
    obj, created = Highlight.objects.get_or_create(spotid=spotid)
    obj.isHighlighted = not obj.isHighlighted
    obj.lastPressed = timezone.now()
    obj.save()
    
    return JsonResponse({
        "spotid": spotid,
        "newstate": obj.isHighlighted
    })