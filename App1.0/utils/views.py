from random import randint, choices

from django.utils import timezone
from django.shortcuts import render
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core.validators import validate_email, ValidationError
from django.views.generic import View
from django.http import JsonResponse
from django.utils.encoding import force_bytes, force_str #force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.files.storage import default_storage



from .models import City, State, Country

# Create your views here.

# function to generate OTP
def generate_otp():
    otp = ""
    for _ in range(4):
        otp += str(randint(1, 9))
    return otp

# Email validate
def is_email(string):
    try:
        validate_email(string)
        return True
    except ValidationError:
        return False


# set secured url
def get_secured_url(request):
    if request.is_secure():
        return "https://"
    else:
        return "http://"


def send_email(obj, message, template, request):
    message.update({
        "domain": get_secured_url(
            request) + request.META["HTTP_HOST"]
    })
    email_message = render_to_string("email/" + template, message)
    send_mail(
        settings.EMAIL_WELCOME_MESSAGE,
        email_message,
        settings.DEFAULT_FROM_EMAIL,
        [obj.email],
        fail_silently=False,
        html_message=email_message
    )


# decode data
def decode_data(input_data):
    uid = force_str(urlsafe_base64_decode(input_data))
    return uid


# encode data
def encode_data(input_data):
    uid = urlsafe_base64_encode(force_bytes(input_data))
    return uid


# Send OTP function
def send_otp(obj, retry=None):
    otp = generate_otp()
    obj.otp = otp
    obj.otp_created_at = timezone.now()
    obj.save()
    # mobile_number = obj.mobile
    # sms_message = "Your OTP to login with Zewellers is " + otp + \
        # ". Valid for 30 minutes. Never share your OTP with anyone. - Thanks, Zewellers Team"
    # result = send_sms(sms_message, mobile_number, retry)
    return {'ErrorCode':'000'}

def is_ajax(request):
        return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'        

# City View for json dropdown
class CityView(View):

    def get(self, request, id):
        state = State.objects.get_state(id)
        cities = list(City.objects.filter(state=state).values("id", "name"))
        data = {
            "cities": cities
        }
        return JsonResponse(data)


# State View for State dropdown
class StateView(View):

    def get(self, request, id):
        country = Country.objects.get_country(id)
        states = list(State.objects.filter(
            country=country).values("id", "name"))
        data = {
            "states": states
        }
        return JsonResponse(data)


#upload file
def upload_file(instance, filename, dir_name):
    name = filename.name.replace(" ", "_")
    url = "%s/%d/%s" % (dir_name,int(instance.id), name)
    file_name = default_storage.save(url, filename)
    return file_name
