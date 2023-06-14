from django.urls import path
from . import views

urlpatterns = [
    path("profiles", views.profiles, name="profiles"),
    path("profile/<str:pk>", views.profile_detail, name="profile_detail"),
    path("user-account", views.user_account, name="user_account"),
    path("edit-user-account", views.edit_user_account, name="edit_user_account"),
    path("create-skill", views.create_skill, name="create_skill"),
    path("update-skill/<str:pk>", views.update_skill, name="update_skill"),
    path("delete-skill/<str:pk>", views.delete_skill, name="delete_skill"),
]
