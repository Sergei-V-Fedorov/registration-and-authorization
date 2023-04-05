from django.urls import path
from .views import LoginFormView, LogoutFormView, register_view, ProfileView, ProfileFormEdit

urlpatterns = [
    path("login/", LoginFormView.as_view(), name='login'),
    path("logout/", LogoutFormView.as_view(), name='logout'),
    path("register/", register_view, name='register'),
    path("profile/", ProfileView.as_view(), name='profile'),
    path("profile/<int:pk>/edit/", ProfileFormEdit.as_view(), name='profile-edit')
]
