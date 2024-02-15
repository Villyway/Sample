from django.shortcuts import render
from django.views.generic import View

from inward.forms import InWardForm

# Create your views here.
class CreateInward(View):
    template_name = "inward/create.html"

    def get(self,request):
        context = {
            "form":InWardForm()
        }
        return render(request,self.template_name,context)