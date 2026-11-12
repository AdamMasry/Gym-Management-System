from django import forms

from accounts.forms import BootstrapFormMixin
from accounts.models import User

from .models import TrainerProfile


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
