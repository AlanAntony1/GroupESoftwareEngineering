from django.shortcuts import render

# Create your views here.

from django.contrib.auth.decorators import login_required

from .ai_matcher import parse_schedule_csv, recommend_for_schedule


@login_required  # schedules are personal; require authentication
def match_schedule(request):
    """
    AI Schedule Matcher:
    Upload a schedule CSV and get recommended parking for each class.
    """
    context = {}

    if request.method == "POST" and "schedule_file" in request.FILES:
        schedule_file = request.FILES["schedule_file"]
        items = parse_schedule_csv(schedule_file)
        recommendations = recommend_for_schedule(items)
        context["recommendations"] = recommendations

    return render(request, "scheduleMatcher/matcher.html", context)
