from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import LoginForm

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("manage/", views.admin_panel, name="admin_panel"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="accounts/login.html",
            authentication_form=LoginForm,
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("profile/", views.profile_edit, name="profile_edit"),
    path("manage/users/", views.user_list, name="user_list"),
    path("manage/users/<int:pk>/", views.user_edit, name="user_edit"),
    path("manage/users/new/", views.user_create, name="user_create"),
]