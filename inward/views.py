from django.shortcuts import render
from django.views.generic import View

from inward.forms import InWardForm

# Create your views here.
class CreateInward(View):
    template_name = "inward/create.html"
    form_calss = InWardForm()

    def get(self,request):
        context = {
            "form":self.form_calss
        }
        return render(request,self.template_name,context)
    
    def post(self,request):
        print(request.POST)
        return render(request,self.template_name)
