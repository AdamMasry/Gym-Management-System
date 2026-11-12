from django.contrib import admin

from .models import MembershipPlan


@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = ["name", "duration_days", "price", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name"]
