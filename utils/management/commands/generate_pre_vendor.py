import json


from django.core.management.base import BaseCommand
from django.conf import settings

# from utils.models import City, State, Country
from vendors.models import Vendor


class Command(BaseCommand):
    help = """Generate Pre Data"""

    def add_location(self):
        # {'name': 'Aamron Technology', 'contect': 8047307462, 'al_contect': '', 'email': '', 'gst_no': '27AIMPU0542K1ZU', '': ''}

        with open('./static/csvjson.json') as f:
            data = json.load(f)
            
            for i in data:
                # print(i)
                if i['gst_no']:
                    if Vendor.objects.filter(gst_no=i['gst_no']).exists():
                       pass
                    else:
                        Vendor.objects.create(gst_no=str(i['gst_no']))

                # v.comany_name = i.get('name', '')

                # if isinstance(i.get('contect'), str):
                #     v.mobile = i.get('contect', '')
                # else:
                #     v.mobile = str(i.get('contect', ''))

                # v.mobile1 = i.get('al_contect', '')
                # v.email = i.get('email', '')

                # # Set other fields accordingly

                # v.save()
                
                
        
    def handle(self, *args, **kwargs):
        self.add_location()
