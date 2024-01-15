import datetime

from itertools import chain

from django.db import models
from django.db.models import Q
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
            return self.active().get(part_no=part_no)
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
    
