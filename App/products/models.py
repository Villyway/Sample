from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save

from base.models import Base
from .managers import ProductManager, AttributeManager
from utils.views import upload_file
from utils.constants.choices import State


# Create slug by this Method
def create_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    instance_model = type(instance)
    qs = instance_model.objects.filter(slug=slug)
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


# pre-save Method for slug
def pre_save_slug_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


class Categories(Base):
    name = models.CharField(max_length=30, null=True, blank=True)
    slug = models.SlugField()

    def __str__(self):
        return self.slug


# Unit
class Unit(Base):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    

#Product
class Product(Base):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100, null=True, blank=True)
    category = models.ForeignKey(
        Categories, on_delete=models.SET_NULL, null=True, related_name='product_category')
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


pre_save.connect(pre_save_slug_receiver, sender=Categories)
