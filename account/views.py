from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account.models import User
from account.serializers import UserSerializer



class UserLoginView(APIView):
    def get(self, request):
        email = request.GET.get("email")
        password = request.GET.get("password")
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
