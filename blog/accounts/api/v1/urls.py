from django.urls import path
from blog.accounts.api.v1.views import (
    SignUpAPIView,
    SignInAPIView,
    ChangePasswordAPIView,
    UpdateProfileAPIView,
)

urlpatterns = [
    path('sign-up/', SignUpAPIView.as_view(), name='register'),
    path('sign-in/', SignInAPIView.as_view(), name='sign_in'),
    path('change-password/', ChangePasswordAPIView.as_view(), name='change_password'),
    path('update-profile/', UpdateProfileAPIView.as_view(), name='update_profile')
]