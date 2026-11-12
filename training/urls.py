from django.urls import path

from . import views

urlpatterns = [
    path("trainers/", views.trainer_list, name="trainer_list"),
    path("trainers/<int:pk>/", views.trainer_detail, name="trainer_detail"),
    path("trainers/me/edit/", views.edit_my_profile, name="edit_my_profile"),
    path("trainers/me/members/", views.my_members, name="my_members"),
    path("trainers/assign/", views.assign_trainer, name="assign_trainer"),
    path("trainers/assign/<int:pk>/remove/", views.unassign_trainer, name="unassign_trainer"),
]
