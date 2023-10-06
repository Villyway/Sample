import json
import pandas as pd
import string

from django.core.management.base import BaseCommand
from django.conf import settings

from products.models import Product, Categories, PartQuality, BOMItem
from utils.views import generate_part_code


class Command(BaseCommand):
    help = """Generate Pre Data"""

    def add_item(self):

        excel_data_df = pd.read_excel('static/record2.xlsx', engine='openpyxl')
        json_data = excel_data_df.to_json(orient='records')

        item_data = json.loads(json_data)
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


    def add_bom(self):
        excel_data_df = pd.read_excel('static/record3.xlsx', engine='openpyxl')
        json_data = excel_data_df.to_json(orient='records')

        item_data = json.loads(json_data)

        # for i in item_data:
            # product = Product.objects.all()
            # for i in product:
                # if i.code:
                    # i.code = i.code.strip()
                    # i.save()
                
        for i in item_data:
            
            if i['SR.NO'] == 137 or i['SR.NO'] == 218 or i['SR.NO'] == 299 or i['SR.NO'] == 463 or i['SR.NO'] == 831 or i['SR.NO'] == 879 or i['SR.NO'] == 857 or i['SR.NO'] == 935 or i['SR.NO'] == 1074 or i['SR.NO'] == 1075 or i['SR.NO'] == 1076 or i['SR.NO'] == 1077 or i['SR.NO'] == 1145 or i['SR.NO'] == 1146 or i['SR.NO'] == 1147 or i['SR.NO'] == 1152 or i['SR.NO'] == 1153 or i['SR.NO'] == 1154 or i['SR.NO'] == 1155 or i['SR.NO'] == 1224 or i['SR.NO'] == 1225 or i['SR.NO'] == 1226 or i['SR.NO'] == 1227 or i['SR.NO'] == 1249 or i['SR.NO'] == 1250 or i['SR.NO'] == 1251 or i['SR.NO'] == 1254 or i['SR.NO'] == 1253: 
                pass
            else:
                if i['QTY'] == None:
                    print(i)
                    BOMItem.objects.get_or_create(
                        product = Product.objects.get(code = i['MAIN PART']),
                        component = Product.objects.get(part_no = i['CHILD PART']),
                        quantity = 1,
                        category = i['CATAGORIES']
                    )
                else:
                    print(i)
                    BOMItem.objects.get_or_create(
                        product = Product.objects.get(code = i['MAIN PART']),
                        component = Product.objects.get(part_no = i['CHILD PART']),
                        quantity = i['QTY'],
                        category = i['CATAGORIES']
                    )
                
            


    def handle(self, *args, **kwargs):
        # self.add_item()
        self.add_bom()
