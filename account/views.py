from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account.models import User
from account.serializers import UserSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.conf import settings
from .utils import send_activation_email

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
            user = serializer.create(serializer.validated_data)
             
            uid=urlsafe_base64_encode(force_bytes(user.id))
            
            token= default_token_generator.make_token(user)
            activation_link = reverse('activate', kwargs={'uid': uid, 'token': token})
            activation_url= f'{settings.SITE_DOMAIN}{activation_link}'
            print("activation link--",activation_link)
            print("activation url--",activation_url)
            send_activation_email(user.email, activation_url)
            

            return Response({"message": "email verification sent successfully.","data":UserSerializer(user).data,"activation_link":activation_link}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
