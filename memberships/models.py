from datetime import timedelta
from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from accounts.models import User


class MembershipPlan(models.Model):
    name = models.CharField(max_length=100, unique=True)
    duration_days = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"), message="Price must be greater than zero.")],
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Only active plans are shown to members.",
    )

    class Meta:
        ordering = ["price", "name"]

    def __str__(self):
        return f"{self.name} ({self.duration_days} days)"


class Membership(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        FROZEN = "FROZEN", "Frozen"
        EXPIRED = "EXPIRED", "Expired"

    class Action(models.TextChoices):
        SUBSCRIBE = "SUBSCRIBE", "Subscribe"
        RENEW = "RENEW", "Renew"
        FREEZE = "FREEZE", "Freeze"

    MAX_FREEZE_DAYS = 30

    member = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="membership",
        limit_choices_to={"role": User.Role.MEMBER},
    )
    plan = models.ForeignKey(
        MembershipPlan,
        on_delete=models.PROTECT,
        related_name="memberships",
    )
    start_date = models.DateField()
    end_date = models.DateField()
    frozen_until = models.DateField(null=True, blank=True)
    last_action = models.CharField(max_length=10, choices=Action.choices, default=Action.SUBSCRIBE)

    class Meta:
        ordering = ["end_date"]

    @property
    def status(self):
        today = timezone.localdate()
        if today > self.end_date:
            return self.Status.EXPIRED
        if self.frozen_until and today < self.frozen_until:
            return self.Status.FROZEN
        return self.Status.ACTIVE

    @property
    def status_label(self):
        return self.Status(self.status).label

    @classmethod
    def subscribe(cls, member, plan):
        """Starts a membership today. The end date is the start date plus the plan duration."""
        if not plan.is_active:
            raise ValidationError("This plan is not available.")
        membership = cls.objects.filter(member=member).first()
        if membership and membership.status != cls.Status.EXPIRED:
            raise ValidationError("You already have a membership. Renew it instead.")
        if membership is None:
            membership = cls(member=member)
        today = timezone.localdate()
        membership.plan = plan
        membership.start_date = today
        membership.end_date = today + timedelta(days=plan.duration_days)
        membership.frozen_until = None
        membership.last_action = cls.Action.SUBSCRIBE
        membership.save()
        return membership

    def renew(self):
        """Extends the end date by the plan duration.

        An expired membership restarts today. A frozen membership cannot be
        renewed twice in a row.
        """
        status = self.status
        if status == self.Status.FROZEN and self.last_action == self.Action.RENEW:
            raise ValidationError("This frozen membership was already renewed. Wait until the freeze ends.")
        duration = timedelta(days=self.plan.duration_days)
        if status == self.Status.EXPIRED:
            self.start_date = timezone.localdate()
            self.end_date = self.start_date + duration
            self.frozen_until = None
        else:
            self.end_date = self.end_date + duration
        self.last_action = self.Action.RENEW
        self.save()

    def freeze(self, days):
        """Pauses the membership for the given days and moves the end date forward by the same days."""
        if self.status == self.Status.EXPIRED:
            raise ValidationError("An expired membership cannot be frozen. Renew it first.")
        if self.status == self.Status.FROZEN:
            raise ValidationError("This membership is already frozen.")
        if days < 1 or days > self.MAX_FREEZE_DAYS:
            raise ValidationError(f"You can freeze for 1 to {self.MAX_FREEZE_DAYS} days.")
        self.frozen_until = timezone.localdate() + timedelta(days=days)
        self.end_date = self.end_date + timedelta(days=days)
        self.last_action = self.Action.FREEZE
        self.save()

    def __str__(self):
        return f"{self.member} - {self.plan.name} ({self.status_label})"