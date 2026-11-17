from django.contrib import admin

from .models import Membership, MembershipPlan


@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = ["name", "duration_days", "price", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name"]


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ["member", "plan", "start_date", "end_date", "status_label"]
    list_filter = ["plan"]
    search_fields = ["member__email", "member__first_name", "member__last_name"]