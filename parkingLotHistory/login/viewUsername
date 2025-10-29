from django.shortcuts import render, redirect

# Hardcoded
USERNAME = "groupE"
PASSWORD = "groupE"

def login_view(request):
    """Login page"""
    error = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username == USERNAME and password == PASSWORD:
            request.session['logged_in'] = True
            return redirect('history')  # Redirect after login
        else:
            error = "Invalid username or password."
    return render(request, "parkingLotHistory/login.html", {"error": error})

def logout_view(request):
    """Logout and clear session"""
    request.session.flush()
    return redirect('login')

def parking_history(request):
    """Protected page: parking lot history"""
    if not request.session.get('logged_in'):
        return redirect('login')  # Redirect if not logged in

    # Example parking data
    parking_data = [
        {"lot": "Lot A", "status": "Full", "time": "10:00 AM"},
        {"lot": "Lot B", "status": "Available", "time": "10:15 AM"},
        {"lot": "Lot C", "status": "Available", "time": "10:30 AM"},
    ]
    return render(request, "parkingLotHistory/history.html", {"parking_data": parking_data})
