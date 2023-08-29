from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save

from base.models import Base
from utils.models import Address

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


# Create your models here.
class Vendor(Base):
    code = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(unique=True, editable=False)
    name = models.CharField(max_length=150, null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    country_code = models.CharField(max_length=4, default="91")
    email = models.EmailField(null=True, blank=True)
    gst_no = models.CharField(max_length=16, unique=True)
    address = models.ManyToManyField(Address, blank=True)

    def __str__(self):
        return self.name
    

pre_save.connect(pre_save_slug_receiver, sender=Vendor)