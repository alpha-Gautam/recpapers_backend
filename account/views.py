from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account.models import User
from django.contrib.auth import login, authenticate, logout
from rest_framework.permissions import AllowAny
from account.serializers import UserSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.conf import settings
from .utils import send_activation_email, send_reset_password_email

@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCookies(APIView):
    permission_classes = [AllowAny]
    def get(self,request):
        return Response({"csrfToken": request.META.get('CSRF_COOKIE', '')}, status=status.HTTP_200_OK)

        # return Response({"message": "CSRF cookie set"})

# @method_decorator(csrf_protect, name="dispatch")
# @method_decorator(csrf_protect, name='dispatch')
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
       
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email).first()
        if user is not None and user.is_active == False:
            uid=urlsafe_base64_encode(force_bytes(user.id))
            token= default_token_generator.make_token(user)
            activation_link = reverse('activate', kwargs={'uid': uid, 'token': token})
            activation_url= f'{settings.SITE_DOMAIN}{activation_link}'
            send_activation_email(user.email, activation_url)
            return Response({"message": "Account is not activated. Please check your email for the activation link."}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            serialize=UserSerializer(user)
            return Response({"message": "Login successful.","data":serialize.data}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)   
    

# @method_decorator(csrf_protect, name='dispatch')
class RegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            print("data:",request.data)
            serializer=UserSerializer(data=request.data)
            if serializer.is_valid():
                # print("serializer-->",serializer.data)
                user=serializer.create(serializer.validated_data)


                uid=urlsafe_base64_encode(force_bytes(user.id))

                token= default_token_generator.make_token(user)
                activation_link = reverse('activate', kwargs={'uid': uid, 'token': token})
                activation_url= f'{settings.SITE_DOMAIN}{activation_link}'
                # print("activation link--",activation_link)
                print("activation url--",activation_url)
                send_activation_email(user.email, activation_url)

                return Response({"message": "email verification sent successfully.","data":f'{user.email}--{user.get_full_name()}',"activation_link":activation_url}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ActivateView(APIView):
    permission_classes = [AllowAny]    
    def get(self, request, uid, token):
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            if user.is_active:
                # return Response({"message": "Account is already activated."}, status=status.HTTP_200_OK)
                return render(request,'account/email_verification_success.html',{'user':user,'status':'already_activated'}, status=status.HTTP_200_OK)
            user.is_active = True
            print('user is activated', user)
            user.save()
            return render(request,'account/email_verification_success.html',{'user':user,'status':'success'}, status=status.HTTP_200_OK)
        else:
            # return Response({"error": "Activation link is invalid or has expired."}, status=status.HTTP_400_BAD_REQUEST)
            return render(request,'account/email_verification_success.html',{'user':user,'status':'invalid'}, status=status.HTTP_200_OK)
        
class UserDetailsView(APIView):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
    
class LogoutView(APIView):
    permission_classes = [AllowAny]
    

    def post(self, request):
        user = request.user
        print('user is logged out', user)
        logout(request)
        return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)
    
class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = default_token_generator.make_token(user)
            reset_link = reverse('reset_password', kwargs={'uid': uid, 'token': token})
            reset_url = f'{settings.SITE_DOMAIN}{reset_link}'
            send_reset_password_email(user.email, reset_url)  # Implement this function to send the email
            return Response({"message": "Password reset link sent to your email."}, status=status.HTTP_200_OK)
        return Response({"message": "Email not found."}, status=status.HTTP_404_NOT_FOUND)

class ResetPasswordPageView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uid, token):
        # Render the password reset page
        print("password reset page opened")
        return render(request, 'account/reset_password_page.html', {'uid': uid, 'token': token})

    def post(self, request, uid, token):
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            new_password = request.data.get('new_password')
            confirm_password = request.data.get('confirm_password')
            if new_password != confirm_password:
                return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)
        return Response({"error": "Reset link is invalid or has expired."}, status=status.HTTP_400_BAD_REQUEST)
    
    
# @method_decorator(csrf_protect, name='dispatch')
class UpdatePasswordView(APIView):
    
    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
        
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')
        if new_password != confirm_password:
            return Response({"error": "New passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)
        if not user.check_password(old_password):
            return Response({"error": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)
    
    
@method_decorator(csrf_protect, name='dispatch')    
class DeleteUserView(APIView):
    def delete(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
        user.delete()
        logout(request)
        return Response({"message": "User account deleted successfully."}, status=status.HTTP_200_OK)