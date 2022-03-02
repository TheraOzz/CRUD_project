from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_user, name="login_user"),
    path("logout/", views.logout_user, name="logout_user"),
    path("signup/", views.signup_user, name="signup_user"),
    path("trainer/create/", views.create, name="create"),
    path("trainer/read/", views.read, name="read"),
    path("trainer/edit/", views.edit, name="edit"),
    path("trainer/update/<int:id>", views.update, name="update"),
    path("trainer/delete/<int:id>", views.delete, name="delete"),
]