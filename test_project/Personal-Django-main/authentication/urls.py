from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from authentication import views

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name="user-register"),
    path('login/', views.UserLoginView.as_view(), name="user-login"),
    path('logout/', views.UserLogoutView.as_view(), name="user-logout"),
    path('profile/', views.CurrentUserProfileView.as_view(), name="user-profile"),
    path('info/', views.UserInfoView.as_view(), name="user-info"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Google 验证器 (2FA)
    path('2fa/status/', views.TwoFactorStatusView.as_view(), name='2fa-status'),
    path('2fa/setup/', views.TwoFactorSetupView.as_view(), name='2fa-setup'),
    path('2fa/confirm/', views.TwoFactorConfirmView.as_view(), name='2fa-confirm'),
    path('2fa/verify-login/', views.TwoFactorVerifyLoginView.as_view(), name='2fa-verify-login'),
    path('2fa/disable/', views.TwoFactorDisableView.as_view(), name='2fa-disable'),
]