from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from accounts.models import User
from accounts.permissions import role_required

from .forms import AssignTrainerForm, TrainerProfileForm
from .models import TrainerAssignment, TrainerProfile


@login_required
def trainer_list(request):
    profiles = TrainerProfile.objects.filter(user__is_active=True).select_related("user")
    return render(request, "training/trainer_list.html", {"profiles": profiles})


@login_required
def trainer_detail(request, pk):
    profile = get_object_or_404(TrainerProfile, pk=pk, user__is_active=True)
    return render(request, "training/trainer_detail.html", {"profile": profile})


@role_required(User.Role.TRAINER)
def edit_my_profile(request):
    profile = TrainerProfile.objects.filter(user=request.user).first()
    if request.method == "POST":
        form = TrainerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect("trainer_detail", pk=profile.pk)
    else:
        form = TrainerProfileForm(instance=profile)
    return render(request, "training/edit_profile.html", {"form": form, "is_new": profile is None})


@role_required(User.Role.TRAINER)
def my_members(request):
    assignments = (
        request.user.assigned_members.filter(member__is_active=True)
        .select_related("member")
        .order_by("member__first_name")
    )
    return render(request, "training/my_members.html", {"assignments": assignments})


@role_required(User.Role.ADMIN)
def assign_trainer(request):
    if request.method == "POST":
        form = AssignTrainerForm(request.POST)
        if form.is_valid():
            TrainerAssignment.objects.update_or_create(
                member=form.cleaned_data["member"],
                defaults={"trainer": form.cleaned_data["trainer"]},
            )
            return redirect("assign_trainer")
    else:
        form = AssignTrainerForm()
    assignments = TrainerAssignment.objects.select_related("member", "trainer").order_by(
        "trainer__first_name", "member__first_name"
    )
    return render(request, "training/assign_trainer.html", {"form": form, "assignments": assignments})


@require_POST
@role_required(User.Role.ADMIN)
def unassign_trainer(request, pk):
    get_object_or_404(TrainerAssignment, pk=pk).delete()
    return redirect("assign_trainer")
