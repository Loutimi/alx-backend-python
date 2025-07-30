from django.urls import path
from django.contrib.auth import views as auth_views
from .views import homepage, dashboard

urlpatterns = [
    path("", homepage, name="homepage"),
    path("dashboard/", dashboard, name="dashboard"),
    path(
        "login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"
    ),
]
