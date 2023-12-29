import json

from django.shortcuts import redirect, render
from django.utils import timezone
from django.contrib.auth import login, logout, update_session_auth_hash
from django.views.generic import View
from django.views.generic.edit import FormView
from django.contrib import messages
from django.http import JsonResponse, Http404
from django.db import transaction
from django.urls import reverse


from users.models import User
from .forms import UserRegisterForm, ChangePasswordForm, ResetPasswordForm
from utils.views import send_email, generate_otp, is_email, send_otp

class Dashboard(View):
    template_name = "base.html"

    def get(self,request):
        return render(request, self.template_name)



class Login(View):
    template_name = "base/login.html"

    def get(self, request):
        if not request.user.is_anonymous:
             return redirect("base:dashboard")
        return render(request, self.template_name)
    
    def post(self, request):
        try:
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = User.objects.user_authentication(username)
            if user is not None and user.check_password(password):
                if user.is_deactivated:
                    messages.error(
                        request, "Your account has been blocked, Please contact BasuriAutomotive Team to activate that.")
                    return redirect("login")
                if user.is_active:
                    login(request, user)
                    messages.success(
                        request, "Logged In!")
                    return redirect("base:dashboard")
                else:
                    if user.email != None and user.email != "":
                        result = send_otp(user)
                        # result["ErrorCode"] = "000"
                        otp = user.otp
                        self.request.session['send_otp'] = user.id
                        message = {
                            "name": user.name,
                            "email": user.email,
                            "otp":  str(otp)
                        }
                        send_email(user, message,
                                   "user_verification_email.html", self.request)
                        messages.success(
                            request, "Your Account is not yet Verified ! Please Verify that by entering OTP sent on your email.")
                        return redirect("base:otp_verify")
                    messages.error(
                        request, "You are not an active user, please activate your account.")
                    return redirect("base:otp-verification")
            else:
                messages.error(
                    request, "There is no user with this credentials.")
                return redirect("login")

        except Exception as e:
            messages.error(
                request, str(e))
            return redirect("login")
        
class Logout(View):
    def get(self, request):
        request.session.flush()
        logout(request)
        return redirect("login")
    
    
class UserRegister(FormView):
    form_class = UserRegisterForm
    template_name = "base/register.html"

    def form_invalid(self, form):
        response = super(UserRegister, self).form_invalid(form)
        if self.request.is_ajax():
            data = form.errors
            return JsonResponse(data, status=400)

    def form_valid(self, form):
        form_data = form.cleaned_data
        try:
            with transaction.atomic():
                user = User()
                user.mobile = form_data['mobile']

                user.first_name = form_data['first_name']
                user.last_name = form_data['last_name']
                user.name = form_data['first_name'] + \
                    " " + form_data['last_name']
                user.email = form_data['email']

                user.set_password(form_data['password1'])
                # user.role = Roles.BUSINESS_OWNER.value
                user.is_active = False
                user.country_code = form_data['country_code']
                user.username = form_data['mobile']
                user.save()
                # group = Group.objects.get(name=Roles.BUSINESS_OWNER.value)
                # user.groups.add(group)
                if user.email != None and user.email != "":
                    # result["ErrorCode"] = "000"
                    # if result["ErrorCode"] == "000":
                    send_otp(user)
                    self.request.session['send_otp'] = user.id
                    otp = user.otp
                    message = {
                        "name": user.name,
                        "email": user.email,
                        "otp": str(otp)
                    }
                    send_email(user, message,
                               "user_verification_email.html", self.request)
                    messages.success(
                        self.request, "Please verify the OTP sent on your email ID and contact number.")
                    data = {
                        "url": reverse("base:otp_verify")
                    }
                    return JsonResponse(data, status=200)
        except Exception as e:
            data = {"message": str(e)}
            return JsonResponse(data, status=500)
        

class ForgotPasswordView(View):
    template_name = "base/forgotpassword.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        try:
            user = request.POST.get("email")
            if is_email(user):
                if User.objects.filter(email=user).exists():
                    user = User.objects.get(email=user)
                    otp = generate_otp()
                    user.otp_created_at = timezone.now()
                    user.otp = otp
                    user.save()
                    message = {
                        "name": user.name,
                        "email": user.email,
                        "otp": otp
                    }
                    send_email(user, message,
                               "forgot_password_verification.html", request)
                    request.session['send_otp'] = user.id
                    request.session["forgot"] = True
                    messages.success(
                        request, 'Please verify the OTP sent on your email ID.')
                    url = "base:otp_verify"
                else:
                    messages.error(request, 'Please check your email ID.')
                    url = "base:forgotpassword"
            else:
                messages.error(request, 'Please enter a valid email ID.')
                url = "base:forgotpassword"
            return redirect(url)

        except Exception as e:
            messages.error(
                request, 'Not able to User verification due to Error : ' + str(e))
            return render(request, self.template_name)


class ResetPasswordView(View):
    template_name = "base/resetpassword.html"
    form_class = ResetPasswordForm
    success_url = "login"

    def get(self, request):
        try:
            if request.session['send_otp'] == None:
                return redirect('login')
            form = self.form_class
            return render(request, self.template_name, {'form': form})
        except:
            return redirect('login')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        try:
            if form.is_valid():
                data = form.cleaned_data
                id = request.session.get('send_otp')
                user = User.objects.single_user(id)
                user.set_password(data['password1'])
                user.save()
                del request.session['send_otp']
                messages.success(
                    request, 'Your password has been updated.')
                return redirect("login")
            else:
                return render(request, self.template_name, {'form': form})

        except Exception as e:
            messages.error(
                request, 'Not able to Reset Password due to Error : ' + str(e))
            return render(request, self.template_name, {'form': form})


class ResendOtp(View):

    def get(self, request):
        try:
            if request.session['send_otp']:
                id = request.session.get('send_otp')
                user = User.objects.single_user(id)
                if user.email:
                    send_otp(user)
                    # result = send_otp(user)
                    # result = result.decode('utf8').replace("'", '"')
                    # result = json.loads(result)
                    # # result["ErrorCode"] = "000"
                    # if result["ErrorCode"] == "000":
                    #     self.request.session['send_otp'] = user.id
                    otp = user.otp
                    self.request.session['send_otp'] = user.id
                    message = {
                        "name": user.name,
                        "email": user.email,
                        "otp": str(otp)
                    }
                    send_email(user, message,
                               "user_verification_email.html", self.request)
                    messages.success(request, "Resend otp successfully!")
                else:
                    result = send_otp(user)
                    result = result.decode('utf8').replace("'", '"')
                    result = json.loads(result)
                    # result["ErrorCode"] = "000"
                    if result["ErrorCode"] == "000":
                        self.request.session['send_otp'] = user.id
                    messages.success(request, "Resend otp successfully!")
                return redirect("base:otp_verify")
        except Exception as e:
            messages.error(request, str(e))
            return redirect("base:otp_verify")


class ChangePassword(FormView):
    form_class = ChangePasswordForm
    template_name = 'base/password-change.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        self.request.user.is_temp_password = False
        self.request.user.save()
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, 'Your password has been changed.')
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return "/dashboard/"


class VerifyOtp(View):
    template_name = "base/otp_verify.html"

    def get(self, request):
        if request.session.get('send_otp') == None:
            return redirect('base:forgotpassword')
        return render(request, self.template_name)

    def post(self, request):
        try:
            otp = request.POST.get("otp")
            id = request.session.get('send_otp')
            user = User.objects.get(pk=id)
            start = user.otp_created_at
            end = timezone.now()
            time = end - start

            if time.seconds < 300:
                if user.otp == otp:
                    if user.is_active:
                        url = "base:resetpassword"
                    else:
                        user.is_active = True
                        if request.session.get('forgot') == True:
                            user.save()
                            url = "base:resetpassword"
                            del request.session['forgot']
                        else:
                            del request.session['send_otp']
                            login(request, user)
                            url = "base:dashboard"
                    user.otp = None
                    user.otp_created_at = None
                    user.save()

                    messages.success(request, 'OTP verified successfully.')
                    return redirect(url)
                else:
                    messages.error(request, 'OTP did not matched.')
                    return redirect("base:otp_verify")
            else:
                del request.session['send_otp']
                messages.error(
                    request, 'OTP is expired, Please generate the new one')
                return redirect("base:forgotpassword")
        except Exception as e:
            messages.error(
                request, str(e))
            return redirect("base:forgotpassword")
