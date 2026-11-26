from django import forms

from accounts.forms import BootstrapFormMixin
from accounts.models import User

from .models import TrainerProfile, GymClass


class UserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, user):
        name = user.get_full_name()
        return f"{name} ({user.email})" if name else user.email


class TrainerProfileForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = TrainerProfile
        fields = ["specialty", "bio"]
        widgets = {"bio": forms.Textarea(attrs={"rows": 5})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["specialty"].help_text = "For example: strength training, yoga, weight loss."
        self._style_fields()


class AssignTrainerForm(BootstrapFormMixin, forms.Form):
    member = UserChoiceField(
        queryset=User.objects.filter(role=User.Role.MEMBER, is_active=True).order_by("first_name")
    )
    trainer = UserChoiceField(
        queryset=User.objects.filter(role=User.Role.TRAINER, is_active=True).order_by("first_name")
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()

class GymClassForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = GymClass
        fields = [
            "name",
            "day",
            "class_time",
            "duration_minutes",
            "capacity",
        ]

        widgets = {
            "class_time": forms.TimeInput(
                attrs={"type": "time"},
                format="%H:%M",
            ),
            "duration_minutes": forms.NumberInput(
                attrs={"min": 1}
            ),
            "capacity": forms.NumberInput(
                attrs={"min": 1}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["duration_minutes"].help_text = (
            "Duration in minutes."
        )
        self.fields["capacity"].help_text = (
            "Maximum number of members. Must be at least 1."
        )
        self._style_fields()
