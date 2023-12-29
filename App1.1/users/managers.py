from django.contrib.auth.models import UserManager as AbstractUserManager
from django.db.models import Q

from utils.constants.choices import Roles


class UserManager(AbstractUserManager):

    def get_queryset(self):
        return super().get_queryset().order_by('-date_joined')

    def no_superuser(self):
        return self.filter(is_superuser=False)

    def active(self):
        return self.filter(is_active=True)

    def all_users(self, user=None, **kwargs):
        fields = kwargs.get("fields", None)
        if user:
            qs = self.no_superuser().exclude(id=user.id)
        else:
            qs = self.no_superuser()
        if fields and qs:
            qs = self.user_selected_fields(fields=fields, qs=qs)
        return qs

    def single_user(self, id):
        try:
            return self.get(id=id)
        except:
            return None

    def user_authentication(self, username):
        if self.filter(Q(username=username) | Q(email=username) | Q(mobile=username)).exists():
            user = self.get(
                Q(username=username) | Q(email=username) | Q(mobile=username))
            return user
        else:
            return None

    def user_selected_fields(self, fields, qs=None):
        try:
            if qs:
                return qs.values(*fields)
            else:
                return self.active().values(*fields)
        except:
            return None

    def check_if_exists(self, id):
        return self.filter(id=id).exists()
    
    def super_admin(self):
        return self.filter(is_superuser=True)

    # def business_owner(self):
    #     return self.filter(role=Roles.BUSINESS_OWNER.value)

    # def simple_users(self):
    #     return self.filter(role=Roles.USER.value)
