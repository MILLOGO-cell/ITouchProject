from django.urls import include, path
from rest_framework import routers
from .views import RegisterView,VerifyEmail,LogiAPIView, RequestPasswordResetEmail,PasswordResetView,user_info, UserEditView,get_image_url, UserEditAPIView,ChangePasswordView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
 
urlpatterns = [
    path('creer_compte/', RegisterView.as_view(), name='creer_compte'),
    path('connexion/', LogiAPIView.as_view(), name="connexion"),
    path('moi/', user_info, name="moi"),
    path('change-password/', ChangePasswordView.as_view(), name="changer-password"),
    path('modifier/edit/<int:id>/', UserEditView.as_view(), name='modifier'),
    path('get_image_url/<int:id>/', get_image_url, name='get_image_url'),
    path('verification_email/', VerifyEmail.as_view(), name="verification_email"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('request-reset-email/',RequestPasswordResetEmail.as_view(), name="request-reset-email"),
    path('password-reset/',PasswordResetView.as_view(), name='password-reset'),
]

 