from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("login/", auth_views.LoginView.as_view(), name="login"),

    path("api/send/", views.send_message, name="send_message"),
    path("api/inbox/", views.inbox, name="inbox"),
    path("api/delete-user/<int:id>/", views.delete_user, name="delete_user"),
]
