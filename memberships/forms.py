from django import forms

from accounts.forms import BootstrapFormMixin

from .models import MembershipPlan


class MembershipPlanForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = MembershipPlan
        fields = ["name", "duration_days", "price", "is_active"]
        labels = {"duration_days": "Duration (days)"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].help_text = "For example: Monthly, 3 Months, Annual."
        self._style_fields()
        self.fields["is_active"].widget.attrs["class"] = "form-check-input"
