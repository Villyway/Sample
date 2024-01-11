import os

# import code128
import io
# from PIL import Image, ImageDraw, ImageFont

from random import randint, choices

from django.utils import timezone
from django.shortcuts import render, redirect
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.core.validators import validate_email, ValidationError
from django.views.generic import View
from django.http import JsonResponse
from django.utils.encoding import force_bytes, force_str #force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.files.storage import default_storage

from .models import City, State, Country, Address

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


# def send_email(obj, message, template, request):
#     message.update({
#         "domain": get_secured_url(
#             request) + request.META["HTTP_HOST"]
#     })
#     email_message = render_to_string("email/" + template, message)
#     send_mail(
#         settings.EMAIL_WELCOME_MESSAGE,
#         email_message,
#         settings.DEFAULT_FROM_EMAIL,
#         [obj.email],
#         fail_silently=False,
#         html_message=email_message,
#     )

# Not able to User verification due to Error : EmailMessage.__init__() got an unexpected keyword argument 'html_message'
def send_email(obj, message, template, request, email_subject=None, to_email=None, attachment_path=None):
    message.update({
        "domain": get_secured_url(request) + request.META["HTTP_HOST"]
    })
    
    # Render the email content from the template
    email_message = render_to_string("email/" + template, message)

    if to_email:
        from_email=to_email
    else:
        from_email= settings.DEFAULT_FROM_EMAIL
    
    if email_subject:
        subject = email_subject
    else:
        subject = settings.EMAIL_WELCOME_MESSAGE

    # Create an EmailMessage object
    email = EmailMultiAlternatives(
        to=[obj.email],
        from_email= from_email,
        subject = subject,
    )
    email.attach_alternative(email_message,"text/html")

    # Attach a file to the email if attachment_path is provided
    if attachment_path:
        with open(attachment_path, 'rb') as file:
            email.attach_file(attachment_path)

    # Send the email
    email.send()



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
        if state.name == 'Other':
            cities = list(City.objects.filter(name='Other').values("id", "name"))
        else:
            cities = list(City.objects.filter(state=state).values("id", "name"))
            other = cities.append(list(City.objects.filter(name='Other').values("id", "name"))[0])
        data = {
            "cities": cities
        }
        return JsonResponse(data)


# State View for State dropdown
class StateView(View):

    def get(self, request, id):
        country = Country.objects.get_country(id)
        if country.name != 'Other':
            states = list(State.objects.filter(
                country=country).values("id", "name"))
            states.append(list(State.objects.filter(name='Other').values("id", "name"))[0])
        else:
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


# Barcode generater
class BarCode:

    def generate(self,barcode_param, barcode_text, path, file_name):
        # path = os.path.join(settings.MEDIA_ROOT,path)
        # print("hi")
        # if not os.path.exists(path):
                # print("hi")
                # os.makedirs(path, exist_ok=True)
        # path = path + file_name
        # # original image
        # barcode_image = code128.image(barcode_param, height=100)

        # # empty image for code and text - it needs margins for text
        # w, h = barcode_image.size
        # margin = 30
        # new_h = h +(2*margin) 

        # new_image = Image.new( 'RGB', (w, new_h), (255, 255, 255))

        # # put barcode on new image
        # new_image.paste(barcode_image, (0, margin))

        # # object to draw text
        # draw = ImageDraw.Draw(new_image)

        # # draw text
        # fnt = ImageFont.truetype("static/fonts/arial/arial.ttf", 15)
        # draw.text( (10, new_h - 20), barcode_text, fill=(0, 0, 0), font=fnt)  # 

        # # save in file 
        # new_image.save(path, 'PNG')

        # barcode_bytes = io.BytesIO()
        # new_image.save(barcode_bytes, "PNG")
        # barcode_bytes.seek(0)
        # data = barcode_bytes.getvalue()
        return True


def generate_part_code(id,version,quality,compny_name="KI"):
    id = str(id)
    if len(id) == 1:
        id = "000" + str(id)
    elif len(id) == 2:
        id = "00" + str(id)
    elif len(id) == 3:
        id = "0" + str(id)
    else:
        id = str(id)
    return compny_name + str(version) + quality + str(id)


def generate_order_dispatch_no(id):
    # KIDN000001			
    id = str(id)
    if len(id) == 1:
        id = "00000" + str(id)
    elif len(id) == 2:
        id = "0000" + str(id)
    elif len(id) == 3:
        id = "000" + str(id)
    elif len(id) == 4:
        id = "00" + str(id)
    elif len(id) == 5:
        id = "0" + str(id)
    else:
        id = str(id)
    return "KISO" + id


class DeleteAddress(View):

    def get(self,request,id):

        address = Address.objects.get(id = id)
        address.is_active = False
        address.save()
        return redirect(request.META.get('HTTP_REFERER'))