from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

# from products.models import Product
from users.models import User
from utils.constants import Roles


class Command(BaseCommand):
    help = """Generate Groups for shopBasuri"""

    def handle(self, *args, **kwargs):
        # content_type_product = ContentType.objects.get_for_model(Product)
        content_type_user = ContentType.objects.get_for_model(User)

        group_manager, created = Group.objects.get_or_create(
            name=Roles.MANAGER.value)
        group_operator, created = Group.objects.get_or_create(
            name=Roles.OPERATOR.value)
        group_customer, created = Group.objects.get_or_create(
            name = Roles.CUSTOMER.value)


        
        

        # self.stdout.write("Group created for Manager.")

        
        # self.stdout.write("Group created for operator.")

        
        # self.stdout.write("Group created for QC Validator.")

        
        # self.stdout.write("Group created for QC Manager.")

        
        # self.stdout.write("Group created for Business Owner.")
