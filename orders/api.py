from rest_framework.views import APIView
from rest_framework.response import Response

from orders.models import OrderDetails, OrderOfProduct


class CreateOrderApi(APIView):

    def post(self, request):

        return 0


