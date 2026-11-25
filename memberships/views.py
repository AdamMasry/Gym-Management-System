
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from accounts.models import User
from accounts.permissions import role_required

from .forms import (
    FreezeForm,
    MembershipPlanForm,
    SubscribeForm,
    PaymentMethodForm,
)
from .models import Membership, MembershipPlan, Payment


@login_required
def plan_list(request):
    plans = MembershipPlan.objects.all()

    if request.user.role != User.Role.ADMIN:
        plans = plans.filter(is_active=True)

    return render(
        request,
        "memberships/plan_list.html",
        {"plans": plans},
    )


@role_required(User.Role.ADMIN)
def plan_create(request):
    if request.method == "POST":
        form = MembershipPlanForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("plan_list")
    else:
        form = MembershipPlanForm()

    return render(
        request,
        "memberships/plan_form.html",
        {"form": form, "is_new": True},
    )


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

    return render(
        request,
        "memberships/plan_form.html",
        {"form": form, "is_new": False},
    )


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
                "error": (
                    f"The plan {plan.name} has members and cannot be "
                    "deleted. Mark it inactive instead."
                ),
            },
        )

    return redirect("plan_list")


@role_required(User.Role.MEMBER)
def my_membership(request):
    membership = (
        Membership.objects
        .filter(member=request.user)
        .select_related("plan")
        .first()
    )

    payment_form = PaymentMethodForm()

    return render(
        request,
        "memberships/my_membership.html",
        {
            "membership": membership,
            "payment_form": payment_form,
        },
    )


@role_required(User.Role.MEMBER)
def subscribe(request):
    if request.method == "POST":
        form = SubscribeForm(request.POST)

        if form.is_valid():
            plan = form.cleaned_data["plan"]
            payment_method = form.cleaned_data["payment_method"]

            try:
                with transaction.atomic():
                    membership = Membership.subscribe(
                        request.user,
                        plan,
                    )

                    Payment.objects.create(
                        member=request.user,
                        membership=membership,
                        plan=plan,
                        amount=plan.price,
                        payment_method=payment_method,
                    )

            except ValidationError as error:
                form.add_error(None, error.messages[0])

            except Exception:
                form.add_error(
                    None,
                    "The payment could not be recorded. Please try again.",
                )

            else:
                return redirect("my_membership")

    else:
        form = SubscribeForm()

    return render(
        request,
        "memberships/subscribe.html",
        {"form": form},
    )


@require_POST
@role_required(User.Role.MEMBER)
def renew_membership(request):
    membership = get_object_or_404(
        Membership.objects.select_related("plan"),
        member=request.user,
    )

    form = PaymentMethodForm(request.POST)

    if not form.is_valid():
        return render(
            request,
            "memberships/my_membership.html",
            {
                "membership": membership,
                "payment_form": form,
            },
        )

    try:
        with transaction.atomic():
            membership.renew()

            Payment.objects.create(
                member=request.user,
                membership=membership,
                plan=membership.plan,
                amount=membership.plan.price,
                payment_method=form.cleaned_data["payment_method"],
            )

    except ValidationError as error:
        return render(
            request,
            "memberships/my_membership.html",
            {
                "membership": membership,
                "payment_form": form,
                "error": error.messages[0],
            },
        )

    except Exception:
        return render(
            request,
            "memberships/my_membership.html",
            {
                "membership": membership,
                "payment_form": form,
                "error": "The payment could not be recorded. Please try again.",
            },
        )

    return redirect("my_membership")


@role_required(User.Role.MEMBER)
def freeze_membership(request):
    membership = get_object_or_404(
        Membership.objects.select_related("plan"),
        member=request.user,
    )

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

    return render(
        request,
        "memberships/freeze.html",
        {"form": form, "membership": membership},
    )


@role_required(User.Role.ADMIN)
def membership_list(request):
    memberships = (
        Membership.objects
        .select_related("member", "plan")
        .order_by("member__first_name")
    )

    return render(
        request,
        "memberships/membership_list.html",
        {"memberships": memberships},
    )


@role_required(User.Role.MEMBER)
def payment_history(request):
    payments = (
        Payment.objects
        .filter(member=request.user)
        .select_related("plan", "membership")
    )

    return render(
        request,
        "memberships/payment_history.html",
        {"payments": payments},
    )


@role_required(User.Role.MEMBER)
def invoice_detail(request, pk):
    payment = get_object_or_404(
        Payment.objects.select_related(
            "member", "plan", "membership"
        ),
        pk=pk,
        member=request.user,
    )

    return render(
        request,
        "memberships/invoice.html",
        {"payment": payment},
    )
