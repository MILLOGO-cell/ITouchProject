from django.urls import include, path
from rest_framework import routers
from .views import RegisterView,VerifyEmail,LogiAPIView, RequestPasswordResetEmail,PasswordResetView,user_info, UserEditView,get_image_url, UserEditAPIView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
 
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LogiAPIView.as_view(), name="login"),
    path('user_info/', user_info, name="user_info"),
    path('users/edit/<int:id>/', UserEditView.as_view(), name='user_edit'),
    path('get_image_url/<int:id>/', get_image_url, name='get_image_url'),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('request-reset-email/',RequestPasswordResetEmail.as_view(), name="request-reset-email"),
    path('password-reset/',PasswordResetView.as_view(), name='password-reset'),
]

 