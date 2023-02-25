from django.urls import path
from . import views
from django.urls import reverse

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name = "register"),
    path("email-verify/", views.VerifyEmail.as_view(), name = "email-verify"),
    path("login/", views.LoginAPIView.as_view(), name = "login"),
    path("logout/", views.LogoutAPIView.as_view(), name = "logout"),
    path("request-reset-password/", views.PasswordResetView.as_view(), name = "password-reset"),
    path("password-reset/<uidb64>/<token>/", views.PasswordTokenCheckView.as_view(), name = "password-reset-confirm"),
    path("password-reset-complete/", views.SetNewPasswordView.as_view(), name = "password-reset-complete"),
    path("users/<int:pk>", views.UserDetailView.as_view(), name="user"),
    

]