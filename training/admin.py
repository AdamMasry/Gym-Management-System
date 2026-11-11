from django.contrib import admin

from .models import TrainerAssignment, TrainerProfile


@admin.register(TrainerProfile)
class TrainerProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "specialty"]
    search_fields = ["user__email", "user__first_name", "user__last_name", "specialty"]


@admin.register(TrainerAssignment)
class TrainerAssignmentAdmin(admin.ModelAdmin):
    list_display = ["member", "trainer", "assigned_at"]
    search_fields = ["member__email", "trainer__email"]
