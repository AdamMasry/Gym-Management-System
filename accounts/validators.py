from django.core.exceptions import ValidationError


class ComplexityValidator:
    """Requires an uppercase letter, a digit and a special character."""

    def validate(self, password, user=None):
        errors = []

        # At least one uppercase letter.
        if not any(char.isupper() for char in password):
            errors.append("Your password must contain at least one uppercase letter.")

        # At least one digit.
        if not any(char.isdigit() for char in password):
            errors.append("Your password must contain at least one number.")

        # At least one character that is not a letter or digit.
        if all(char.isalnum() for char in password):
            errors.append("Your password must contain at least one special character.")

        # Report every missing requirement in a single error.
        if errors:
            raise ValidationError(errors)

    def get_help_text(self):
        return "Your password must contain an uppercase letter, a number and a special character."
