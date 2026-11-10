from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

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