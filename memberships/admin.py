
from django.contrib import admin

from .models import Membership, MembershipPlan, Payment


@admin.register(MembershipPlan)
class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = ["name", "duration_days", "price", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name"]


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = [
        "member",
        "plan",
        "start_date",
        "end_date",
        "status_label",
    ]
    list_filter = ["plan"]
    search_fields = [
        "member__email",
        "member__first_name",
        "member__last_name",
    ]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        "invoice_number",
        "member",
        "plan",
        "amount",
        "payment_method",
        "payment_date",
    ]
    list_filter = ["payment_method", "payment_date", "plan"]
    search_fields = [
        "invoice_number",
        "member__email",
        "member__first_name",
        "member__last_name",
    ]
    readonly_fields = ["invoice_number", "payment_date"]
    ordering = ["-payment_date"]
