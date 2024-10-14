from django.urls import ( path, )
from accounts.views import (
    RegisterUserView, VerifyUserEmailView,
    LoginUserView, TestAuthenticationView, PasswordResetRequestView,
    PasswordResetConfirmView, SetNewPasswordView, LogoutUserView,
    GoogleOauthSignInView, GithubOauthSignInView,
)
from rest_framework_simplejwt.views import ( TokenRefreshView, )

# Authentication endpoints
auth_patterns = [
    path('sign_in/', LoginUserView.as_view(), name='login'),
    path('sign_up/', RegisterUserView.as_view(), name='register'),
    path('sign_out/', LogoutUserView.as_view(), name='logout'),
]

# Email verification endpoints
verification_patterns = [
    path('email/verify/', VerifyUserEmailView.as_view(), name='verify-email'),
]

# Password management endpoints
password_patterns = [
    path('password/reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('password/new/', SetNewPasswordView.as_view(), name='set-new-password'),
]

# OAuth endpoints
oauth_patterns = [
    path('oauth/google/', GoogleOauthSignInView.as_view(), name='google'),
    path('oauth/github/', GithubOauthSignInView.as_view(), name='github'),
]

# Token endpoints
token_patterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# Combine all patterns
urlpatterns = (
    auth_patterns +
    verification_patterns +
    password_patterns +
    oauth_patterns +
    token_patterns + 
    [path('dashboard/', TestAuthenticationView.as_view(), name='dashboard')]
)