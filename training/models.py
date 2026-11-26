from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from accounts.models import User
from django.core.validators import MinValueValidator

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

class GymClass(models.Model):
    class Day(models.TextChoices):
        MONDAY = "MON", "Monday"
        TUESDAY = "TUE", "Tuesday"
        WEDNESDAY = "WED", "Wednesday"
        THURSDAY = "THU", "Thursday"
        FRIDAY = "FRI", "Friday"
        SATURDAY = "SAT", "Saturday"
        SUNDAY = "SUN", "Sunday"

    trainer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="gym_classes",
        limit_choices_to={"role": User.Role.TRAINER},
    )

    name = models.CharField(max_length=100)

    day = models.CharField(
        max_length=3,
        choices=Day.choices,
    )

    class_time = models.TimeField()

    duration_minutes = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
    )

    capacity = models.PositiveIntegerField(
        validators=[
            MinValueValidator(
                1,
                message="Capacity must be greater than zero.",
            )
        ],
    )

    class Meta:
        ordering = ["day", "class_time", "name"]

    def clean(self):
        super().clean()

        if self.trainer_id and self.trainer.role != User.Role.TRAINER:
            raise ValidationError(
                {"trainer": "Only trainers can create classes."}
            )

    def __str__(self):
        return f"{self.name} - {self.get_day_display()}"
