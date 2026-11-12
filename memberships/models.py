from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


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
