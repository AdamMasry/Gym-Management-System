from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.core.exceptions import ValidationError
from .models import User


class BootstrapFormMixin:
    """Gives every input Bootstrap's form-control class."""

    def _style_fields(self):
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class SignUpForm(BootstrapFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self.fields["password1"].help_text = (
            "Use 8 or more characters with an uppercase letter, a number and a special character."
        )
        self.fields["password2"].label = "Confirm password"
        self.fields["password2"].help_text = ""
        self._style_fields()


class LoginForm(BootstrapFormMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()
class ProfileForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone", "photo"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self._style_fields()


class AdminUserForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone", "role", "is_active"]

    def __init__(self, *args, **kwargs):
        self.acting_user = kwargs.pop("acting_user")
        super().__init__(*args, **kwargs)
        self._style_fields()
        self.fields["is_active"].widget.attrs["class"] = "form-check-input"
        for name in ("first_name", "last_name", "phone"):
            self.fields[name].required = False

    def clean(self):
        cleaned = super().clean()
        for name in ("first_name", "last_name", "phone"):
            if not cleaned.get(name):
                cleaned[name] = getattr(self.instance, name)
        if self.instance.pk == self.acting_user.pk:
            if cleaned.get("role") != User.Role.ADMIN:
                raise ValidationError("You cannot change your own role.")
            if not cleaned.get("is_active"):
                raise ValidationError("You cannot deactivate your own account.")
        return cleaned
    
class UserCreateForm(BootstrapFormMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["email", "first_name", "last_name", "phone", "role"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()