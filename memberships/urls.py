from django.urls import path

from . import views

urlpatterns = [
    path("plans/", views.plan_list, name="plan_list"),
    path("plans/new/", views.plan_create, name="plan_create"),
    path("plans/<int:pk>/edit/", views.plan_edit, name="plan_edit"),
    path("plans/<int:pk>/delete/", views.plan_delete, name="plan_delete"),
    path("membership/", views.my_membership, name="my_membership"),
    path("membership/subscribe/", views.subscribe, name="subscribe"),
    path("membership/renew/", views.renew_membership, name="renew_membership"),
    path("membership/freeze/", views.freeze_membership, name="freeze_membership"),
    path("memberships/", views.membership_list, name="membership_list"),
]
