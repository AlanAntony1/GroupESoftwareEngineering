
from django.shortcuts import render
from .models import Highlight

# Create your views here.
def schedule(request):
    classes = Highlight.objects.all()
    return render(request, 'HighlightButton.html', {"Classes":classes})