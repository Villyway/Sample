from django import forms
from django.contrib.auth import password_validation
from django.core.validators import validate_email
from django.core.validators import RegexValidator

from users.models import User
from utils.views import is_email

class UserRegisterForm(forms.Form):
    mobile_regex = RegexValidator(
        regex=r'^[6-9][0-9]{9}', message="Mobile number must be entered with code in the format: 9999999999. It must start with 6, 7, 8, 9")
    first_name = forms.CharField(max_length=75, strip=True, required=True, label='First Name',
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name *','autofocus':'',}))
    last_name = forms.CharField(max_length=75, strip=True, required=False, label='Last Name',
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    email = forms.CharField(required=False, label='Email ', strip=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}))
    mobile = forms.CharField(
        required=True, max_length=14, label="Mobile No.", widget=forms.NumberInput(attrs={"class": "form-control", "type": "tel"}), validators=[mobile_regex])
    country_code = forms.CharField(required=True,
                                   widget=forms.HiddenInput())
    password1 = forms.CharField(required=True, label=("Password"),
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password *'}))
    password2 = forms.CharField(required=True, label=("Password Confirmation"),
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password *'}))
    terms_and_condition = forms.BooleanField(
        required=True, label="Terms and Condition", widget=forms.CheckboxInput(attrs={'style': 'width:15px;height:15px;'}))
    
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        self.fields["terms_and_condition"].initial = True

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    "The password fields didn't match.")
        return password2

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        country_code = self.cleaned_data.get('country_code')
        if User.objects.filter(mobile__iexact=mobile).exists():
            if User.objects.get(mobile=mobile).role == Roles.USER.value:
                return mobile
            raise forms.ValidationError(
                "Business with this mobile number already exist !")
        return mobile

    def clean_password(self):
        password = self.cleaned_data.get('password1')
        password_validation.validate_password(password)
        return password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email != "" and email != None:
            if is_email(email):
                if User.objects.filter(email__iexact=email).exists():
                    raise forms.ValidationError(
                        "User with this email already exist !")
            else:
                raise forms.ValidationError("Your Email wasn't valid !")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password1')
        password_validation.validate_password(password)
        return password


class ResetPasswordForm(forms.Form):

    password1 = forms.CharField(required=True, label=("Password"),
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(required=True, label=("Password Confirmation"),
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    "The password fields didn't match.")
        return password2

    def clean_password(self):
        password = self.cleaned_data.get('password1')
        password_validation.validate_password(password)
        return password
    

class ChangePasswordForm(forms.Form):
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
        'password_incorrect': "Your old password was entered incorrectly. Please enter it again.",
    }

    old_password = forms.CharField(
        label="Old Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autofocus': True, 'class': 'form-control'}),
    )

    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )

    new_password2 = forms.CharField(
        label="Confirm Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user

    

