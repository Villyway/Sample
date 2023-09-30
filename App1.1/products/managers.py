import datetime

from itertools import chain

from django.db import models
from django.db.models import Q
from django.db.models import Sum



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
