from datetime import datetime
from decimal import Decimal

from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View, FormView
from django.db import transaction

from inward.forms import InWardForm
from utils.views import is_ajax

from purchase.models import PurchaseOrder, PurchaseItem
from inward.models import Inward, InwardItems

# Create your views here.
class CreateInward(FormView):
    
    form_class = InWardForm
    template_name = "inward/create.html"
    success_url = "/products/list/"

    def auto_inward_no(self):
        if Inward.objects.all().count() >= 1:
            inward = Inward.objects.first()
            
            import re
            id = str(int(re.sub('KIN','',inward.inward_no))+1)
            if len(id) == 1:
                id = "000" + str(id)
            elif len(id) == 2:
                id = "00" + str(id)
            elif len(id) == 3:
                id = "0" + str(id)
            else:
                id = str(id)
            print("KIN"+id)
            return "KIN"+id
        else:
            return "KIN0001"

    def form_invalid(self, form):
        response = super(CreateInward,self).form_invalid(form)
        if is_ajax(self.request):
            data = form.errors
            return JsonResponse(data, status=400)
        else:
            return response
    

    def form_valid(self, form):
                
        response = super(CreateInward, self).form_valid(form)
        if is_ajax(self.request):
            form_data = form.cleaned_data
            # transaction.atomic() used because when generate any error then cancle all saved transaction of this class .
            with transaction.atomic():
                po_no = form_data['po_no']
                bill_no = form_data['bill_no']
                bill_date = form_data['bill_date']
                remarks = form_data['remarks']
                po_obj_id = [item for item in self.request.POST.getlist('select[]') if item != '']
                qty_list = [item for item in self.request.POST.getlist('quantity[]') if item != '']

                po = PurchaseOrder.objects.get_po_by_po_no(po_no)

                # Save Inward
                inward = Inward()
                inward.inward_no = self.auto_inward_no()
                inward.purchase_order = po
                inward.remarks = remarks
                inward.save()

                # Saved process of inward item
                for po_item_id, qty in zip(po_obj_id, qty_list):
                    item = PurchaseItem.objects.get(id=po_item_id)
                    inward_item = InwardItems()
                    inward_item.inward = inward
                    inward_item.chalan_no = bill_no
                    inward_item.received_item = item.part
                    inward_item.qty = qty
                    inward_item.uom = item.part.umo
                    inward_item.invoice_date = bill_date
                    inward_item.save()

                    reciv_qty = item.recived_qty + Decimal(inward_item.qty)
                    item.recived_qty = reciv_qty

                    if reciv_qty == item.qty:
                        item.status = True

                    item.save()
                    
                    # All item recived then Close Po.
                    if PurchaseItem.objects.filter(po=po, status=True).count() == PurchaseItem.objects.filter(po=po).count():
                        po.status = False
                        po.close_date = datetime.now()
                        po.save()
            

            return JsonResponse({})
        else:
            return response


class InwardList(View):
    
    template_name = "inward/list.html"

    def get(self, request):
        inwards = Inward.objects.all()
        context = {
            "inwards":inwards
        }
        return render(request, self.template_name, context)