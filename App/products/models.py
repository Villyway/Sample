from django.db import models


from base.models import Base
from .managers import ProductManager, AttributeManager
from utils.views import upload_file
from utils.constants.choices import State



# Unit
class Unit(Base):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    

#Product
class Product(Base):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    umo = models.ForeignKey(
        Unit, on_delete=models.CASCADE, related_name='product_unit',)
    specification = models.TextField(blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True, default=0)
    minimum_stock_level = models.IntegerField(blank=True, null=True, default=0)
    rack_no = models.IntegerField(blank=True, null=True, default=0)
    tray_no = models.IntegerField(blank=True, null=True, default=0)
    image = models.URLField(max_length=500, blank=True, null=True)
    state = models.CharField(
        max_length=25, choices=State.choices(), default=State.IN_REVIEW.value)

    objects = ProductManager()

    def __str__(self):
        return self.code
    
    def save_image_url(self, image, file_url):
        image = upload_file(self, image,"products/"+ self.code)
        image = file_url + '/media/' + image
        self.image = image
        self.save()
        return True


# Model for Attribute
class Attribute(Base):
    name = models.CharField("Name", max_length=50)

    def __str__(self):
        return self.name


# Model for Property
class ProductAttribute(Base):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product_property',)
    attribute = models.ForeignKey(
        Attribute, on_delete=models.SET_NULL, null=True, related_name='property_attribute')
    value = models.CharField(max_length=150)

    objects = AttributeManager()

    def __str__(self):
        return self.attribute.name

