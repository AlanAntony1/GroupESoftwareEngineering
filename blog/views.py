from django.shortcuts import render
from .models import Post

# Create your views here.
def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {"posts":posts})

from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()          # create the new user
            login(request, user)        # log them in automatically (optional)
            return redirect("home")     # send to homepage after signup
    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form})
