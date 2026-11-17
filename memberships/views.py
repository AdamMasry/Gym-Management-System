from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from accounts.models import User
from accounts.permissions import role_required

from .forms import FreezeForm, MembershipPlanForm, SubscribeForm
from .models import Membership, MembershipPlan


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
    plan = get_object_or_404(MembershipPlan, pk=pk)
    try:
        plan.delete()
    except ProtectedError:
        return render(
            request,
            "memberships/plan_list.html",
            {
                "plans": MembershipPlan.objects.all(),
                "error": f"The plan {plan.name} has members and cannot be deleted. Mark it inactive instead.",
            },
        )
    return redirect("plan_list")


@role_required(User.Role.MEMBER)
def my_membership(request):
    membership = Membership.objects.filter(member=request.user).select_related("plan").first()
    return render(request, "memberships/my_membership.html", {"membership": membership})


@role_required(User.Role.MEMBER)
def subscribe(request):
    if request.method == "POST":
        form = SubscribeForm(request.POST)
        if form.is_valid():
            try:
                Membership.subscribe(request.user, form.cleaned_data["plan"])
            except ValidationError as error:
                form.add_error(None, error.messages[0])
            else:
                return redirect("my_membership")
    else:
        form = SubscribeForm()
    return render(request, "memberships/subscribe.html", {"form": form})


@require_POST
@role_required(User.Role.MEMBER)
def renew_membership(request):
    membership = get_object_or_404(Membership.objects.select_related("plan"), member=request.user)
    try:
        membership.renew()
    except ValidationError as error:
        return render(
            request,
            "memberships/my_membership.html",
            {"membership": membership, "error": error.messages[0]},
        )
    return redirect("my_membership")


@role_required(User.Role.MEMBER)
def freeze_membership(request):
    membership = get_object_or_404(Membership.objects.select_related("plan"), member=request.user)
    if request.method == "POST":
        form = FreezeForm(request.POST)
        if form.is_valid():
            try:
                membership.freeze(form.cleaned_data["days"])
            except ValidationError as error:
                form.add_error(None, error.messages[0])
            else:
                return redirect("my_membership")
    else:
        form = FreezeForm()
    return render(request, "memberships/freeze.html", {"form": form, "membership": membership})


@role_required(User.Role.ADMIN)
def membership_list(request):
    memberships = Membership.objects.select_related("member", "plan").order_by("member__first_name")
    return render(request, "memberships/membership_list.html", {"memberships": memberships})