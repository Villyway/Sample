from rest_framework.views import APIView
from rest_framework.response import Response

from orders.serializers import OrderOfProductCreateSerializer

class CreateOrderApi(APIView):
    
    def post(self, request):
        response_data = {}
        try:
            serializer = OrderOfProductCreateSerializer(
                        data=request.data, context={"request": request})
            if serializer.is_valid(raise_exception=True):
                serializer_response = serializer.save()
                if serializer_response["status"]:
                    response_data["message"] = "Business has been successfully registered."
                    response_data['status'] = True
                    response_data['order_no']= serializer_response["order_no"]
            else:
                error = next(iter(serializer.errors))
                response_data["message"] = serializer.errors[str(
                    error)][0]
                response_data["status"] = False
            return Response(response_data)

        except Exception as e:
            response_data['message'] = str(e)
            response_data['status'] = False
            return Response(response_data)

        


