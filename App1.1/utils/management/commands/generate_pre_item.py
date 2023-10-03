import json
import pandas as pd

from django.core.management.base import BaseCommand
from django.conf import settings

from products.models import Product, Categories, PartQuality
from utils.views import generate_part_code


class Command(BaseCommand):
    help = """Generate Pre Data"""

    def add_item(self):

        excel_data_df = pd.read_excel('records.xlsx', engine='openpyxl')
        json_data = excel_data_df.to_json(orient='records')


        item_data = json.loads(json_data)

        # df = pd.read_excel('./static/records.xlsx', engine='openpyxl')
        # item_data = pd.to_json(orient='records')
        # item_data = json.loads(item_data)

        for i in item_data:
            print(i)
            category_obj, created = Categories.objects.get_or_create(
                name__iexact= i['category'],
                defaults={
                    'name': i['category'],                    
                },
                is_active =True
            )
            item_obj, created = Product.objects.get_or_create(
                code = i['item_code'],
                name = i['item_name'],
                category = category_obj,
                version = i['item_version'],
                quality_type = PartQuality.objects.get(code = i['quality_code']),
                is_active = True
            )
            item_obj.part_no = generate_part_code(item_obj.id,item_obj.version, item_obj.quality_type.code)
            item_obj.save()
            




        # with open('./static/location.json') as f:
        #     data = json.load(f)
        # country, created = Country.objects.get_or_create(
        #     name="India",
        #     code="IN"
        # )
        # for state in data['state']:
        #     state_obj, created = State.objects.get_or_create(
        #         name=state['name'],
        #         code=state['code'],
        #         country=country
        #     )

        #     for city in state['city']:
        #         city_obj, created = City.objects.get_or_create(
        #             name=city,
        #             state=state_obj
        #         )

    def handle(self, *args, **kwargs):
        self.add_item()
