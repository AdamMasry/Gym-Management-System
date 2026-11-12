from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm
# Register your models here.
from .models import User

class UserAddForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email", "first_name", "last_name", "phone", "role")

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = UserAddForm
    ordering = ["email"]
    list_display = ["email", "first_name", "last_name", "role", "is_active"]
    list_filter = ["role", "is_active"]
    search_fields = ["email", "first_name", "last_name"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "phone")}),
        ("Role and access", {"fields": ("role", "is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "first_name", "last_name", "phone", "role", "password1", "password2"),
        }),
    )