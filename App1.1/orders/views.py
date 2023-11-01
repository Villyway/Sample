from django.shortcuts import render

# Create your views here.
from datetime import datetime

from django.views.generic import View


class Dashboard(View):
    template_name = "orders/dashboard.html"

    def get(self,request):

        return render(request,self.template_name)