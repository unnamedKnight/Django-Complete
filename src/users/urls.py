from django.urls import path
from . import views

urlpatterns = [
    path("register", views.RegistrationView.as_view(), name="register"),
    path("activate/<uidb64>/<token>/", views.verification, name="activate"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_request, name="logout"),
]
