from django.urls import path
from blog.accounts.api.v1.views import (
    SignUpAPIView,
    SignInAPIView,
    ChangePasswordAPIView,
    RetrieveUpdateProfileAPIView,
)

app_name = 'accounts'

urlpatterns = [
    path('sign-up/', SignUpAPIView.as_view(), name='sign_up'),
    path('sign-in/', SignInAPIView.as_view(), name='sign_in'),
    path('change-password/', ChangePasswordAPIView.as_view(), name='change_password'),
    path('retrieve-update-profile/', RetrieveUpdateProfileAPIView.as_view(), name='retrieve_update_profile')
]