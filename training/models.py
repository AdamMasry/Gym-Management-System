from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from accounts.models import User


class TrainerProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="trainer_profile",
        limit_choices_to={"role": User.Role.TRAINER},
    )
    specialty = models.CharField(max_length=100)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.email} ({self.specialty})"


class TrainerAssignment(models.Model):
    member = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="trainer_assignment",
        limit_choices_to={"role": User.Role.MEMBER},
    )
    trainer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assigned_members",
        limit_choices_to={"role": User.Role.TRAINER},
    )
    assigned_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.trainer.role != User.Role.TRAINER:
            raise ValidationError({"trainer": "This user is not a trainer."})
        if self.member.role != User.Role.MEMBER:
            raise ValidationError({"member": "Only members can be assigned a trainer."})

    def __str__(self):
        return f"{self.member} -> {self.trainer}"
