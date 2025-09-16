from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account.models import User
from account.serializers import UserSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect

@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCookies(APIView):
    def get(self,request):
        return Response({"csrfToken": request.META.get('CSRF_COOKIE', '')}, status=status.HTTP_200_OK)

        # return Response({"message": "CSRF cookie set"})

@method_decorator(csrf_protect, name="dispatch")
class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            return Response({"message": "Login successful.","data":UserSerializer(user).data}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)


class UserRegisterView(APIView):
    def post(self, request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully.","data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
