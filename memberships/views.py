from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from accounts.models import User
from accounts.permissions import role_required

from .forms import MembershipPlanForm
from .models import MembershipPlan


@login_required
def plan_list(request):
    plans = MembershipPlan.objects.all()
    if request.user.role != User.Role.ADMIN:
        plans = plans.filter(is_active=True)
    return render(request, "memberships/plan_list.html", {"plans": plans})


@role_required(User.Role.ADMIN)
def plan_create(request):
    if request.method == "POST":
        form = MembershipPlanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("plan_list")
    else:
        form = MembershipPlanForm()
    return render(request, "memberships/plan_form.html", {"form": form, "is_new": True})


@role_required(User.Role.ADMIN)
def plan_edit(request, pk):
    plan = get_object_or_404(MembershipPlan, pk=pk)
    if request.method == "POST":
        form = MembershipPlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            return redirect("plan_list")
    else:
        form = MembershipPlanForm(instance=plan)
    return render(request, "memberships/plan_form.html", {"form": form, "is_new": False})


@require_POST
@role_required(User.Role.ADMIN)
def plan_delete(request, pk):
    get_object_or_404(MembershipPlan, pk=pk).delete()
    return redirect("plan_list")
