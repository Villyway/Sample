from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (UserRegister,
                    Logout,
                    VerifyOtp,
                    Dashboard,
                    ResetPasswordView,
                    ForgotPasswordView,
                    ResendOtp, ChangePassword
                    )

from base.api import UserLoginView

app_name = "base"

urlpatterns = [
    # path("register/", UserRegister.as_view(), name="register"),
    path("dashboard/", login_required(Dashboard.as_view()), name="dashboard"),
    path("logout/", login_required(Logout.as_view()), name="logout"),
    path("otp-verification/", VerifyOtp.as_view(), name="otp_verify"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgotpassword"),
    path("reset-password/", ResetPasswordView.as_view(), name="resetpassword"),
    path("resend/", ResendOtp.as_view(), name="resend-otp"),
    path('password/change/', login_required(ChangePassword.as_view()),
         name='change-password'),
    path('simple-login/', UserLoginView.as_view(), name="simple-login"),


]