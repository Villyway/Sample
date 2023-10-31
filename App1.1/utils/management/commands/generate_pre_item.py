import json
# import pandas as pd
import string

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction


from products.models import Product, Categories, PartQuality, BOMItem
from utils.views import generate_part_code
from inventry.models import SimpleStockUpdte
from utils.constants import StockTransection


a = [
    {"name":"SOLDRE WIRE RFC TYPE", "category":"Consumable","quality":"C-Common","stock":"28"},
    {"name":"ASTRAL VETRA INSTANT ADHESIVE (FEVI KWICK)", "category":"Consumable","quality":"C-Common","stock":"14"},
    {"name":"ASTRAL BOND TITE SUPER STRENTH", "category":"Consumable","quality":"C-Common","stock":"13"},
    {"name":"ASTRAL BOND GRIP XR", "category":"Consumable","quality":"C-Common","stock":"11"},
    {"name":"ASTRAL THRED LOCKER", "category":"Consumable","quality":"C-Common","stock":"4"},
    {"name":"COFFEE", "category":"Consumable","quality":"C-Common","stock":"3"},
    {"name":"TEA", "category":"Consumable","quality":"C-Common","stock":"13"},
    {"name":"REWINDERS & CONNECTOR- IECCO RFC-101", "category":"Consumable","quality":"C-Common","stock":"2"},
    {"name":"BERG STRIP STATE", "category":"Consumable","quality":"C-Common","stock":"400"},
    {"name":"FILLWEL BYTANE GAS CARTRIDGE", "category":"Consumable","quality":"C-Common","stock":"2"},
    {"name":"3/8 & 6/8 CONTROLLER STRIP", "category":"Consumable","quality":"C-Common","stock":"2375"}
     ]

class Command(BaseCommand):
    help = """Generate Pre Data"""

    # def add_item(self):

    #     excel_data_df = pd.read_excel('static/item_data.xlsx', engine='openpyxl')
    #     json_data = excel_data_df.to_json(orient='records')

    #     item_data = json.loads(json_data)
    #     for i in item_data:
    #         category_obj, created = Categories.objects.get_or_create(
    #             name__iexact= i['category'],
    #             defaults={
    #                 'name': i['category'],                    
    #             },
    #             is_active =True
    #         )
    #         if i['quality'].strip() == "C-COMMAN":
    #             i['quality'] = "C-COMMON"
    #         if i['quality'].strip() == "L-COMMAN":
    #             i['quality'] = "L-COMMON"
    #         item_obj, created = Product.objects.get_or_create(
    #             code = i['item_code'],
    #             name = i['item_name'],
    #             category = category_obj,
    #             version = i['item_version'],
    #             quality_type = PartQuality.objects.get(name = i['quality'].strip()),
    #             is_active = True
    #         )
    #         item_obj.part_no = generate_part_code(item_obj.id,item_obj.version, item_obj.quality_type.code)
    #         item_obj.save()


    # def add_bom(self):
    #     excel_data_df = pd.read_excel('static/record4.xlsx', engine='openpyxl')
    #     json_data = excel_data_df.to_json(orient='records')

    #     item_data = json.loads(json_data)

    #     # for i in item_data:
    #         # product = Product.objects.all()
    #         # for i in product:
    #             # if i.code:
    #                 # i.code = i.code.strip()
    #                 # i.save()
                
    #     for i in item_data:
            
    #         if i['QTY'] == None:
    #             BOMItem.objects.get_or_create(
    #                 product = Product.objects.get(code = i['MAIN PART']),
    #                 component = Product.objects.get(part_no = i['CHILD PART']),
    #                 quantity = 1,
    #                 category = i['CATAGORIES']
    #             )
               

    #         else:
    #             print(i)
    #             BOMItem.objects.get_or_create(
    #                 product = Product.objects.get(code = i['MAIN PART']),
    #                 component = Product.objects.get(part_no = i['CHILD PART']),
    #                 quantity = i['QTY'],
    #                 category = i['CATAGORIES']
    #             )
    
    def create_product(self, i, quality_obj, category_obj):
        # if i['code']:
        #     i['code'] = i['code'].strip()
        item_obj, created = Product.objects.get_or_create(
                name = i['name'].strip(),
                )
        # item_obj.code = i['code']
        item_obj.category = category_obj
        item_obj.version = "1"
        item_obj.quality_type = quality_obj
        item_obj.is_active = True
        item_obj.part_no = generate_part_code(item_obj.id,item_obj.version, item_obj.quality_type.code)
        item_obj.save()
        return item_obj
                
    # def add_pre_item(self):

    #     excel_data_df = pd.read_excel('static/exportdata.xlsx', engine='openpyxl')
    #     json_data = excel_data_df.to_json(orient='records')

    #     item_data = json.loads(json_data)
    #     for i in item_data:
    #         print(i)
            
    #         # Create Category:
    #         category_obj, created = Categories.objects.get_or_create(
    #             name__iexact= i['category__name'],
    #             defaults={
    #                 'name': i['category__name'],                    
    #             },
    #             is_active =True
    #         )

    #         # # create Part Quality
    #         quality_obj, created = PartQuality.objects.get_or_create(
    #                 name = i['quality_type__name'].strip(),
    #                 code = i['quality_type__name'].split("-")[0]
    #             )
            
    #         if i['code']:
    #             # Create Main Part
    #             product = self.create_product(i, quality_obj, category_obj)
            
    #         else:
    #             # Get Main Part
    #             # main_product = Product.objects.by_code(i['main'].strip())

    #             # Create child Part
    #             product = self.create_product(i, quality_obj, category_obj)

    #             # # Create Bom
    #             # BOMItem.objects.get_or_create(
    #             #     product = main_product,
    #             #     component = product,
    #             #     quantity = int(i['bom_qty']),
    #             #     category = i['bom_category']
    #             # )
            
    # def add_stock(self):
    #     excel_data_df = pd.read_excel('static/stock_update.xlsx', engine='openpyxl')
    #     json_data = excel_data_df.to_json(orient='records')

    #     item_data = json.loads(json_data)

    #     for i in item_data:
    #         try:
    #             print(i)
    #             product = Product.objects.get(name=i['name'])
    #             if i['STOCK']:
    #                 product.stock = i['STOCK']
    #             else:
    #                 product.stock = 0
    #             product.save()
    #         except:
    #             pass
            
    def add_pre_item_by_json(self):
        for i in a:
            category_obj, created = Categories.objects.get_or_create(
                name__iexact= i['category'],
                defaults={
                    'name': i['category'],                    
                },
                is_active =True
            )

            # # create Part Quality
            quality_obj, created = PartQuality.objects.get_or_create(
                    name = i['quality'].strip(),
                    code = i['quality'].split("-")[0]
                )

            part = self.create_product(i, quality_obj, category_obj)

            with transaction.atomic():
                stock = SimpleStockUpdte()
                stock.part = part
                stock.old_stock = part.stock
                stock.received_by = "rupesh"
                stock.received_qty = int(i['stock'])
                stock.transection_type = StockTransection.CR.value
                stock.quantity_on_hand = part.stock + int(i['stock'])
                stock.save()

                part.stock = stock.quantity_on_hand
                part.save() 
                


    def handle(self, *args, **kwargs):
        self.add_pre_item_by_json()
        # self.add_pre_item()
        # self.add_stock()
        # self.add_item()
        # self.add_bom()
