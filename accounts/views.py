from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .forms import AdminUserForm, ProfileForm
from .forms import AdminUserForm, ProfileForm, UserCreateForm
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

@login_required
def profile_edit(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "accounts/profile_edit.html", {"form": form})


@role_required(User.Role.ADMIN)
def user_list(request):
    users = User.objects.order_by("email")
    role = request.GET.get("role", "")
    if role in User.Role.values:
        users = users.filter(role=role)
    return render(request, "accounts/user_list.html", {
        "users": users,
        "roles": User.Role.choices,
        "selected_role": role,
    })


@role_required(User.Role.ADMIN)
def user_edit(request, pk):
    target = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = AdminUserForm(request.POST, instance=target, acting_user=request.user)
        if form.is_valid():
            form.save()
            return redirect("user_list")
    else:
        form = AdminUserForm(instance=target, acting_user=request.user)
    return render(request, "accounts/user_edit.html", {"form": form, "target": target})

@role_required(User.Role.ADMIN)
def user_create(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("user_list")
    else:
        form = UserCreateForm()
    return render(request, "accounts/user_create.html", {"form": form})