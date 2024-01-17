import os
import json
from csv import DictReader
from io import TextIOWrapper

from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic import View
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, Http404
from django.template.loader import render_to_string
from django.core.files.storage import default_storage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from .models import (Product, Attribute, ProductAttribute,
                      Categories, PartQuality, BOMItem, VendorWithProductData
                    )
from .forms import ProductForm, FileUploadForm
from utils.views import get_secured_url, is_ajax
from .serializers import InwordOfProductSerializer, ProductSerializer, ProductSerializerWithId
from utils.views import generate_part_code, BarCode
from .resources import ProductResource
from vendors.models import Vendor


# Product Dashboard
class Dashboard(View):
    template_name = "products/dashboard.html"

    def get(self, request):
        total_categories = Categories.objects.all()
        total_product = Product.objects.active().count()
        __item = {}
        for i in total_categories:
           __item[i.name] = Product.objects.category_by_count(i)
        context = {
            "total":total_product,
            "category_by":__item,
            "categories":total_categories
        }

        # product_a = Product.objects.get(code="FLBGC01")
        # bom = product_a.get_bom()
        # Print the BOM
        # for component, quantity in bom.items():
        #     print(f"Component: {component}, Quantity: {quantity}")

        return render(request,self.template_name, context)


# Product List
class ProductList(View):
    template_name = "products/list.html"

    def get(self,request):
        categories = Categories.objects.all()
        products = Product.objects.active()
        results_per_page = 7
        page = request.GET.get('page', 1)
        paginator = Paginator(products, results_per_page)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        context = {
            "products": products,
            "data" : [page,results_per_page],
            "categories":categories

        }
        return render(request, self.template_name, context)

    

# Product Create.
class CreateProduct(FormView):
    form_class = ProductForm
    template_name = "products/create.html"
    success_url = "/products/list/"

    def form_invalid(self, form):
        response = super(CreateProduct, self).form_invalid(form)
        if is_ajax(self.request):
            data = form.errors
            return JsonResponse(data, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(CreateProduct, self).form_valid(form)        
        try:
            if is_ajax(self.request):
                form_data = form.cleaned_data
                with transaction.atomic():
                    product = Product()
                    product.code = form_data['code']
                    product.name = form_data['name']
                    product.category = form_data["category"]
                    product.description = form_data['description']
                    product.umo = form_data['umo']
                    product.specification = form_data['specification']
                    product.stock = form_data['stock']
                    product.minimum_stock_level  = form_data['minimum_stock_level']
                    product.rack_no = form_data['rack_no']
                    product.tray_no = form_data['tray_no']
                    product.created_by = self.request.user.id
                    product.quality_type = form_data['part_quality']
                    product.version = form_data['part_version']                    
                    product.save()

                    product.part_no = generate_part_code(product.id, product.version, product.quality_type.code)
                    product.save()

                    if form_data['image']:
                        product.save_image_url(form_data["image"], get_secured_url(
                                self.request) + self.request.META["HTTP_HOST"])
                        
                    gen_barcode = BarCode()
                    path = "products/"+ product.part_no + "/barcodes/"
                    status = gen_barcode.generate(product.part_no,product.part_no,path, product.name + ".png")
                    product.barcode_image = get_secured_url(self.request) + self.request.META["HTTP_HOST"] +"/media/" + path + product.name + ".png"
                    product.save()
                        
                    
                    
                    messages.success(
                        self.request, "Product added successfully.")
                data = {
                        'message': "Product added successfully.",
                        'url': get_secured_url(
                            self.request) + self.request.META["HTTP_HOST"] + '/products/' + str(product.id) + '/product-property/'
                    }
                return JsonResponse(data)
            else:
                return response
        
        except Exception as e:
            data = {"error": str(e), "status": 403}
            return JsonResponse(data)


#Product Edit
class ProductEditView(FormView):
    form_class = ProductForm
    template_name = "products/edit.html"

    def get_form_kwargs(self):
        product = Product.objects.single_product(
            id= self.kwargs["id"])
        kwargs = super(ProductEditView, self).get_form_kwargs()
        kwargs.update({"product": product, "edit": True})
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super(ProductEditView, self).get_context_data(**kwargs)
        product = Product.objects.single_product(id=self.kwargs["id"])
        context['product'] = product
        context['previous_url'] = self.request.META.get('HTTP_REFERER')
        return context
    
    def form_invalid(self, form):
        super(ProductEditView, self).form_invalid(form)
        messages.error(self.request,form.errors)
        return redirect(self.request.META['HTTP_REFERER'])
    
    def form_valid(self, form):
        form_data = form.cleaned_data
        try:
            with transaction.atomic():
                product = Product.objects.single_product(id = self.kwargs['id'])
                if product.code != form_data['code']:
                    product.code = form_data['code']
                if product.name != form_data['name']:
                    product.name = form_data['name']
                if product.category != form_data['category']:
                    product.category = form_data['category']
                if product.description != form_data['description']:
                    product.description = form_data['description']
                if product.umo != form_data['umo']:
                    product.umo = form_data['umo']
                if product.specification != form_data['specification']:
                    product.specification = form_data['specification']
                if product.stock != form_data['stock']:
                    product.stock = form_data['stock']
                if product.minimum_stock_level != form_data['minimum_stock_level']:
                    product.minimum_stock_level = form_data['minimum_stock_level']
                if product.rack_no != form_data['rack_no']:
                    product.rack_no = form_data['rack_no']
                if product.tray_no != form_data['tray_no']:
                    product.tray_no = form_data['tray_no']
                product.updated_by = self.request.user.id
                product.save()
                if form_data['image']:
                    if product.image:
                        old_image = '/'.join(product.image.split('/')[4:])
                        if default_storage.exists(old_image):
                            default_storage.delete(old_image)
                    product.save_image_url(form_data["image"], get_secured_url(
                            self.request) + self.request.META["HTTP_HOST"])
                return redirect('products:products-list')
            
        except Exception as e:
            messages.error(self.request, str(e))
            return redirect(self.request.META['HTTP_REFERER'])


class ProductProperty(View):
    template_name = "products/attribute.html"

    def get(self, request, id):
        product = Product.objects.single_product(id)
        properties = ProductAttribute.objects.filter(product=product)
        attribute = Attribute.objects.all()
        previous_url = request.META.get('HTTP_REFERER')
        context = {
            "product": product,
            "properties": properties,
            "previous_url": previous_url,
            "attribute": attribute
        }

        return render(request, self.template_name, context)

    def post(self, request, id):
        product = Product.objects.single_product(id)
        try:
            data = json.loads(request.POST.get("data"))
            if data["attribute"] != '' and data["value"] != '':
                attribute = data["attribute"]
                value = data["value"].strip()
                obj, created = Attribute.objects.get_or_create(
                    name__iexact=attribute,
                    defaults={
                        'name': attribute
                    }
                )
                check_same_property = ProductAttribute.objects.match_same_attribute(
                    product=product, attribute=obj)
                if not check_same_property:
                    property_obj = ProductAttribute()
                    property_obj.product = product
                    property_obj.attribute = obj
                    property_obj.value = value
                    property_obj.save()
                    error = None
                else:
                    error = "This property was already add."
            else:
                error = "All fields are required."

            properties = ProductAttribute.objects.filter(product=product)
            html = render_to_string(
                template_name="components/attributes_table.html",
                context={"properties": properties, "error": error}
            )

            data_dict = {
                "data": html
            }
            return JsonResponse(data=data_dict, safe=False)

        except Exception as e:
            data = {
                "error": str(e),
                "status": 500
            }
            return JsonResponse(data)


class RemoveProductProperty(View):

    def post(self, request):
        try:
            property_id = request.POST.get("id")
            property_obj = ProductAttribute.objects.get(id=property_id)
            product = property_obj.product
            properties = ProductAttribute.objects.filter(product=product)
            property_obj.delete()
            html = render_to_string(
                template_name="components/attributes_table.html",
                context={"properties": properties}
            )
            data_dict = {
                "data": html
            }
            return JsonResponse(data=data_dict, safe=False)

        except Exception as e:
            data = {
                "error": str(e),
                "status": 500
            }
            return JsonResponse(data)
       

#Category
class CreateCategories(View):
    template_name = "products/category.html"
    
    def get(self, request):
        categories = Categories.objects.filter(is_active=True)
        previous_url = request.META.get('HTTP_REFERER')
        context = {
            "categories": categories,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        try:
            data = json.loads(request.POST.get("data"))
            if data["category"] != '':
                category = data["category"]
                obj, created = Categories.objects.get_or_create(
                    name__iexact=category,
                    defaults={
                        'name': category
                    },
                    is_active =True
                )
                
            
            categories = Categories.objects.filter(is_active=True)
            html = render_to_string(
                template_name="components/categories_table.html",
                context={"categories": categories}
            )

            data_dict = {
                "data": html
            }
            return JsonResponse(data=data_dict, safe=False)

        except Exception as e:
            data = {
                "error": str(e),
                "status": 500
            }
            return JsonResponse(data)


class RemoveProductCategory(View):

    def post(self, request):
        try:
            category_id = request.POST.get("id")
            category_obj = Categories.objects.get(id=category_id)
            category_obj.is_active = False
            category_obj.save()
            categories = Categories.objects.filter(is_active=True)
            html = render_to_string(
                template_name="components/categories_table.html",
                context={"categories": categories}
            )
            data_dict = {
                "data": html
            }
            return JsonResponse(data=data_dict, safe=False)

        except Exception as e:
            data = {
                "error": str(e),
                "status": 500
            }
            return JsonResponse(data)


class GetProductName(View):

    def get(self, request,id):
        product = InwordOfProductSerializer(Product.objects.single_product(id = id)).data
        data = {
            "product": product
        }
        return JsonResponse(data)
    

#Category
class CreateQuality(View):
    template_name = "products/quality.html"
    
    def get(self, request):
        categories = PartQuality.objects.filter(is_active=True)
        previous_url = request.META.get('HTTP_REFERER')
        context = {
            "categories": categories,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        try:
            data = json.loads(request.POST.get("data"))
            if data["category"] != '' and data["code"] != '':
                category = data["category"]
                code = data["code"]
                description = data["description"]
                obj, created = PartQuality.objects.get_or_create(
                    name__iexact=category,
                    defaults={
                        'name': category,
                        'code': code,
                        'description':description
                    },
                    is_active =True
                )
                
            
            categories = PartQuality.objects.filter(is_active=True)
            html = render_to_string(
                template_name="components/quality_table.html",
                context={"categories": categories}
            )

            data_dict = {
                "data": html
            }
            return JsonResponse(data=data_dict, safe=False)

        except Exception as e:
            data = {
                "error": str(e),
                "status": 500
            }
            return JsonResponse(data)


#Bom List
class BomItemList(View):
    template_name = "bom/bom_list.html"

    def get(self,request):
        # products = BOMItem.objects.values_list('product__name','product__code', 'product__id','product__part_no').distinct()
        products = Product.objects.active().filter(category=Categories.objects.get(id=1)).order_by('id')
        results_per_page = 10
        page = request.GET.get('page', 1)
        paginator = Paginator(products, results_per_page)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        context = {
            "products": products,
            "data" : [page,results_per_page]

        }
        return render(request, self.template_name, context)
    

#Get Bom of Singel Finished Product
class SingelBom(View):
    template_name = "bom/singel_bom.html"

    def get(self,request, id):
        product_a = Product.objects.by_code(id)
        bom = product_a.get_bom(60)
        
        context={
            "part_no": product_a.part_no,
            "name": product_a.name,
            "code":product_a.code,
            "image":product_a.image,
            "stock" : product_a.stock,
            "components" : bom,
            
        }
        
        return render(request, self.template_name,context)
    
class CategoryWiseList(View):
    template_name = "products/category_wise.html"

    def get(self,request, id):
        category = Categories.objects.get(id=id)
        products = Product.objects.category_wise(category)

        page = request.GET.get('page', 1)
        paginator = Paginator(products, 7)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        context = {
            "products": products,
            "category" : category.name
        }
        return render(request, self.template_name, context)


class ExportData(View):
    
    def get(self, request):
        product_resourse = ProductResource()
        queryset = Product.objects.active().order_by('id')
        dataset = product_resourse.export(queryset)
        response = HttpResponse(dataset.csv,content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename="product.csv"'
        return response
    

# Create Bom 
class CreatBOM(View):
    template_name = "bom/create.html"
    form_name = FileUploadForm()
    
    
    def get(self,request):
        
        return render(request,self.template_name,{"form":self.form_name})
    
    def post(self,request):
        bom_file = request.FILES["csv_file"]
        main_part_no = request.POST.get('main_part_no')
        rows = TextIOWrapper(bom_file, encoding="utf-8", newline="")
        with transaction.atomic():
            main_part = Product.objects.by_part_no(main_part_no)
            if main_part:
                for row in DictReader(rows):
                    child_part = Product.objects.by_part_no(row['part_no'])
                    qty = row['qty']
                    bom = BOMItem()
                    bom.product = main_part
                    bom.component = child_part
                    bom.quantity = qty
                    bom.save()
                messages.success(
                    request, "Bom Created successfully"
                )      
            else:
                messages.error(
                    request, "Main Product is Not Found"
                )      
        
        return render(request,self.template_name,{"form":self.form_name})
    

# Row data by Json response
# Singel Product return
class SingleProduct(View):
    
    def get(self, request, id):
        product = ProductSerializer(Product.objects.single_product(id)).data
        data = {"product":product}
        return JsonResponse(data, status=200)


class SingleProductByPartNo(View):
    
    def get(self, request, id):
        product = Product.objects.by_part_no(id)
        if product:
            product = ProductSerializerWithId(product).data
            data = {"product":product}
            return JsonResponse(data, status=200)
        else:
            data = {"product":"NOT FOUND"}
            return JsonResponse(data, status=400)
            

class ProductSearch(View):
    template_name = "components/product-list.html"
    # permission_required = "products.can_access_product"

    def get(self, request):
        try:
            if is_ajax(request):
                query = request.GET.get("query", None)
                category = request.GET.get("category", None)
                if category != '0':

                    item_category = Categories.objects.get(id=category)
                else:
                    item_category = None

                categories = Categories.objects.all()
                products = Product.objects.search(
                    query=query,category = item_category)

                results_per_page = 100
                page = request.GET.get('page', 1)
                paginator = Paginator(products, results_per_page)
                try:
                    products = paginator.page(page)
                except PageNotAnInteger:
                    products = paginator.page(1)
                except EmptyPage:
                    products = paginator.page(paginator.num_pages)
                    
                html = render_to_string(
                    template_name=self.template_name,
                    context={"products": products, "data" : [page,results_per_page], "categories":categories}
                )

                data_dict = {
                    "data": html
                }
                return JsonResponse(data=data_dict, safe=False)

            if request.META.get('HTTP_REFERER'):
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                return redirect("products:list")
        except Exception as e:
            return JsonResponse({"error": str(e)})


# Product Details
class ProductDetails(View):
    template_name = "products/show.html"

    def get(self, request, id):
        product = Product.objects.by_part_no(id)
        price = product.vendorwithproductdata_set.active()
        print(price)

        context = {
            'product' : product,
            'vendors':price
        }

        return render(request,self.template_name, context)


# Add Vendor
# class AddVendorOfProduct(View):

#     template_name = "products/add_vendor.html"
#     form_class = VendorWithProduct

#     def get(self,request,id):
#         product = Product.objects.by_part_no(id)

#         context = {
#             "product":product,
#             "form":self.form_class
#         }

#         return render(request,self.template_name,context)
    
#     def post(self,request,id):
#         if is_ajax(self.request):
#             with transaction.atomic():
#                 vendor = Vendor()
#                 if request.POST.get('comany_name'):
#                     vendor.comany_name = request.POST.get('comany_name')
#                     vendor.save()
#                 else:
#                     if Vendor.objects.filter(id = int(request.POST.get('vendor'))).exists:
#                          vendor = Vendor.objects.get(id = int(request.POST.get('vendor')))
                

#                 product = Product.objects.by_part_no(id)
#                 obj = VendorWithProductData()
#                 obj.vendor = vendor
#                 obj.product = product
#                 obj.price = request.POST.get('price')
#                 obj.save()
#                 messages.success(
#                     self.request, "Order added successfully.")
#             data = {
#                     'message': "Order added successfully.",
#                     'url': request.META.get('HTTP_REFERER')
#                 }
#             return JsonResponse(data)
#         else:
#             return redirect("orders:orders-create")


        

