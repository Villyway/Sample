
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User

# api for user login
class UserLoginView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        response_data = {}
        try:
            username = request.data.get("username")
            password = request.data.get("password")
            user = User.objects.user_authentication(username)
            if user is not None and user.check_password(password):
                refresh = RefreshToken.for_user(user)
                if user.is_deactivated:
                    response_data['message'] = "You have been deactivated by super admin."
                    response_data['status'] = False
                    return Response(response_data)
                if user.is_active:
                    response_data["message"] = "success"
                    response_data["status"] = True
                    
                    response_data['data'] = {
                        'role': user.role,
                        'access': str(refresh.access_token),
                        'refresh': str(refresh),
                        'is_active': user.is_active
                    }
                    response_data['data']['name'] = user.name
                    return Response(response_data)
                else:
                    response_data["status"] = False
                    response_data["message"] = "Please contect to rupesh@krunalindusties.com"
                    return Response(response_data)
            else:
                response_data["message"] = "There is no user with this credentials."
                response_data["status"] = False
                return Response(response_data)
        except Exception as e:
            response_data['message'] = str(e)
            response_data['status'] = False
            return Response(response_data)


