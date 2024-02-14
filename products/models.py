from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save

from base.models import Base
from .managers import ProductManager, AttributeManager, VendorWithProductDataManager
from utils.views import upload_file
from utils.constants.choices import State
from vendors.models import Vendor


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
        return self.name.capitalize()
    

class SubCategory(Base):
    category = models.ForeignKey(
        Categories, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name.capitalize()
    

# Like Export, Asia, Domestic, Comman
class PartQuality(Base):
    name = models.CharField(max_length=30, null=True, blank=True)
    description = models.CharField(max_length=80, null=True, blank=True)
    code = models.CharField(max_length=5, null=True, blank=True)

    def __str__(self):
        return self.name.capitalize()


# Unit
class Unit(Base):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    

#Product
class Product(Base):
    code = models.CharField(max_length=20, null=True, blank=True) # Price List Code
    name = models.CharField(max_length=100, null=True, blank=True)
    category = models.ForeignKey(
        Categories, on_delete=models.SET_NULL, null=True, related_name='product_category')
    description = models.TextField(blank=True, null=True)
    umo = models.ForeignKey(
        Unit, on_delete=models.CASCADE, related_name='product_unit',blank=True, null=True)
    specification = models.TextField(blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    minimum_stock_level = models.IntegerField(blank=True, null=True, default=0)
    rack_no = models.IntegerField(blank=True, null=True, default=0)
    tray_no = models.IntegerField(blank=True, null=True, default=0)
    image = models.URLField(max_length=500, blank=True, null=True)
    state = models.CharField(
        max_length=25, choices=State.choices(), default=State.IN_REVIEW.value)
    version = models.CharField(max_length=20, default="1")
    part_no = models.CharField(max_length=20, null=True, blank=True)
    drowing_file = models.URLField(max_length=500, blank=True, null=True)
    quality_type = models.ForeignKey(
        PartQuality, on_delete=models.SET_NULL, null=True, related_name='quality')
    barcode_image = models.URLField(max_length=500, blank=True, null=True)
    subcategory = models.ForeignKey(
        SubCategory, on_delete=models.SET_NULL, null=True)

    objects = ProductManager()

    def __str__(self):
        return self.part_no +" - " +self.name
    
    def save_image_url(self, image, file_url):
        image = upload_file(self, image,"products/"+ self.part_no + "/images/")
        image = file_url + '/media/' + image
        self.image = image
        self.save()
        return True
    
    def get_bom(self,qty=None):
        # Query the BOMItems related to this product
        bom_items = BOMItem.objects.filter(product=self)
        components = []
        a = 0
        # Create a dictionary to store the components and their quantities
        
        
        # Populate the BOM dictionary
        for bom_item in bom_items:
            bom = {}
            component_image = bom_item.component.image 
            component_name = bom_item.component.name
            component_code = bom_item.component.code
            component_part_no = bom_item.component.part_no
            quantity = bom_item.quantity
            bom['image'] = component_image
            bom['name'] = component_name
            bom['qty'] = quantity
            bom['part_no'] = component_part_no
            bom['code'] = component_code
            bom['stock'] = bom_item.component.stock
            bom['id'] = bom_item.id
            if qty:
                bom['total_req'] = quantity * qty
                bom['availabel'] = bom_item.component.stock - quantity * qty
            components.append(bom)
            a = a + quantity
        components.append(
            {
                'image' : "",
                'name' :"Total",
                'qty' : a,
                'part_no': "",
                'code' : "",
                'stock':"",
            }
        )

        return components


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
    

class BOMItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='bom_items')
    component = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='used_in_bom')
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return str(self.id)
        # return f"{self.quantity} {self.component.name} for {self.product.name}"


class VendorWithProductData(Base):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    objects = VendorWithProductDataManager()

    def __str__(self):
        return str(self.id)

pre_save.connect(pre_save_slug_receiver, sender=Categories)
