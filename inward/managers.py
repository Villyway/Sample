from datetime import datetime


from itertools import chain

from django.db import models
from django.db.models import Q
from django.db.models import Sum

from utils.constants.choices import State



class InWordManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().order_by("-created_at")
    
    def active(self):
        return self.filter(is_active=True)
    
    def single_inword(self, id):
        try:
            return self.active().get(id=id)
        except:
            return None
    
    def inword_selected_fields(self, fields, qs=None):
        try:
            if qs:
                return qs.values(*fields)
            else:
                return self.active().values(*fields)
        except:
            return None
        
    def qc_list(self):
        return self.filter(qc_status=False)
    
    def qc_rejected(self):
        return self.filter(qc_state = State.REJECTED.value)
    
    def qc_approved(self):
        return self.filter(qc_state = State.REJECTED.value)

