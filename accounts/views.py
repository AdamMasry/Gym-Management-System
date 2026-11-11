from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

# Create your views here.
from .forms import SignUpForm
from .models import User
from .permissions import role_required


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # role defaults to Member
            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})


@login_required
def home(request):
    return render(request, "accounts/home.html")


@role_required(User.Role.ADMIN)
def admin_panel(request):
    return render(request, "accounts/admin_panel.html")
