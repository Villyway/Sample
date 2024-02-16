import datetime

from itertools import chain

from django.db import models
from django.db.models import Q, Max
# from django.db.models import Sum


class ProductManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().order_by("-created_at")
    
    def active(self):
        return self.filter(is_active=True)
    
    def single_product(self, id):
        try:
            return self.active().get(id=id)
        except:
            return None
        
    def category_by_count(self,category):
        try:
            return self.active().filter(category=category).count()
        except:
            return None
        
    def category_wise(self,category):
        try:
            return self.active().filter(category=category)
        except:
            return None
    
    def by_code(self,code):
        try:
            return self.active().get(code=code)
        except:
            return None
        
    def by_part_no(self,part_no):
        try:
            return self.active().get(part_no__icontains=part_no)
        except:
            return None
        
    def search(self, query=None, category=None):
        if category != None and query != None:
            qs = self.category_wise(category).filter(Q(name__icontains=query) | Q(
            code__icontains=query) | Q(category__name__icontains=query) | Q(part_no__icontains=query))
        elif category != None and query == None:
            qs = self.category_wise(category)
        
        else:
            qs = self.active().filter(Q(name__icontains=query) | Q(
                code__icontains=query) | Q(category__name__icontains=query) | Q(part_no__icontains=query))
        return qs
    
    def finished_product(self):
        return self.active().filter(category__slug = "finish-goods")
        

class AttributeManager(models.Manager):
    def get_queryset(self):
        return super(AttributeManager, self).get_queryset()

    def search(self, query):
        return self.filter(
            Q(value__icontains=query), is_active=True)

    def property(self, product):
        return self.filter(product=product)

    def get_property(self, pk):
        if self.filter(pk=pk).exists():
            return self.get(pk=pk)
        return None

    def match_same_attribute(self, product, attribute):
        if self.filter(product=product, attribute=attribute).exists():
            return True
        else:
            return False


class VendorWithProductDataManager(models.Manager):

    def get_queryset(self):
        return super(VendorWithProductDataManager, self).get_queryset()
    
    def active(self):
        return self.filter(is_active=True)
    
    def get_vendor_with_product_price(self, vendor):
        return self.active().filter(vendor=vendor)
    
    def get_vendor_product_of_last_price_obj(self,product):
        last_price = self.active().filter(product=product).aggregate(last_price=Max('created_at'))['last_price']
        return self.active().filter(product=product, created_at=last_price).first()

    # def get_lastprice_list(self,vendor):
    #     unique_products = self.get_vendor_with_product_price(vendor).select_related('product').values('product').distinct()

    #     # Iterate through the unique products and fetch the last created price for each
    #     for product_data in unique_products:
    #         product_id = product_data['product']
    #         # Retrieve the product instance
    #         product = Product.objects.get(pk=product_id)
        
    #         # Retrieve the last created price for the current product and vendor
    #         last_price = VendorWithProductData.objects.filter(product=product, vendor=vendor).aggregate(last_price=Max('created_at'))['last_price']
            
    #         # Retrieve the VendorWithProductData instance for the last created price
    #         last_price_instance = VendorWithProductData.objects.filter(product=product, vendor=vendor, created_at=last_price).first()
            
    #         # If a last price instance is found, print the vendor and its last created price
    #         if last_price_instance:
    #             print(f"Vendor: {vendor.comany_name}, Product: {product.name}, Last Created Price: {last_price_instance.price}")
    
