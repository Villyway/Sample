from django.db import models
from django.db.models import Q
from django.utils.text import slugify
from django.db.models.signals import pre_save

from base.models import Base
from utils.models import Address
from utils.constants.choices import State

# Create slug by this Method
def create_slug(instance, new_slug=None):
    slug = slugify(instance.comany_name)
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

    
class VendorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by("-created_at")

    def active(self):
        return self.filter(is_active=True)

    def single_vendor(self, id):
        try:
            return self.active().get(id=id)
        except:
            return None
    
    def search(self, query):
        if query:
            return self.filter(Q(comany_name__icontains=query) |Q(gst_no__icontains=query)
)
        else:
            return self.get_queryset()


#Party Type
class PartyType(Base):
    type = models.CharField(max_length=30, unique=True, blank=True, null=True)

    def __str__(self):
        return self.type


# Create your models here.
class Vendor(Base):
    code = models.CharField(max_length=30, blank=True, null=True)  # KI000001
    type = models.ForeignKey(
        PartyType, on_delete=models.CASCADE, related_name='vendor_type', blank=True, null=True)
    comany_name = models.CharField(max_length=150, null=True, blank=True)
    slug = models.SlugField(unique=True, editable=False)
    primary_contect_name = models.CharField(max_length=150, null=True, blank=True)
    secondary_contect_name = models.CharField(max_length=150, null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    mobile1 = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    email1 = models.EmailField(null=True, blank=True)
    gst_no = models.CharField(max_length=18, null=True, blank=True)
    msme_no = models.CharField(max_length=15, null=True, blank=True)
    bank_name = models.CharField(max_length=150, null=True, blank=True)
    bank_branch_name = models.CharField(max_length=150, null=True, blank=True)
    bank_isfc = models.CharField(max_length=15, null=True, blank=True)
    bank_account_no = models.CharField(max_length=18, null=True, blank=True)
    address = models.ManyToManyField(Address, blank=True)
    is_approved = models.BooleanField(default=False)
    state = models.CharField(
        max_length=25, choices=State.choices(), default=State.IN_REVIEW.value)
    
    objects = VendorManager()

    def __str__(self):
        return str(self.comany_name)
    

pre_save.connect(pre_save_slug_receiver, sender=Vendor)