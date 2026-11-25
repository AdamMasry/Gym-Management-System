
from django import forms

from accounts.forms import BootstrapFormMixin

from .models import Membership, MembershipPlan, Payment


class MembershipPlanForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = MembershipPlan
        fields = ["name", "duration_days", "price", "is_active"]
        labels = {"duration_days": "Duration (days)"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].help_text = (
            "For example: Monthly, 3 Months, Annual."
        )
        self._style_fields()
        self.fields["is_active"].widget.attrs["class"] = "form-check-input"


class SubscribeForm(BootstrapFormMixin, forms.Form):
    plan = forms.ModelChoiceField(
        queryset=MembershipPlan.objects.none(),
        empty_label="Choose a plan",
        label="Membership plan",
    )

    payment_method = forms.ChoiceField(
        choices=Payment.PaymentMethod.choices,
        label="Payment method",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["plan"].queryset = MembershipPlan.objects.filter(
            is_active=True
        )
        self.fields["plan"].label_from_instance = (
            lambda plan: (
                f"{plan.name} - {plan.duration_days} days - {plan.price}"
            )
        )
        self._style_fields()


class PaymentMethodForm(BootstrapFormMixin, forms.Form):
    payment_method = forms.ChoiceField(
        choices=Payment.PaymentMethod.choices,
        label="Payment method",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()


class FreezeForm(BootstrapFormMixin, forms.Form):
    days = forms.IntegerField(
        label="Freeze for (days)",
        min_value=1,
        max_value=Membership.MAX_FREEZE_DAYS,
        help_text=(
            f"Between 1 and {Membership.MAX_FREEZE_DAYS} days. "
            "Your end date moves forward by the same number of days."
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()
