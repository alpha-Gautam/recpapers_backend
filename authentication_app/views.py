from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from .models import student,mentor
from .serializers import StudentSerializer, MentorSerializer
from rest_framework import generics,status
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly


# Create your views here.


# class ListUsers(APIView):
#     """
#     View to list all users in the system.

#     * Requires token authentication.
#     * Only admin users are able to access this view.
#     """
#     # authentication_classes = [authentication.TokenAuthentication]
#     # permission_classes = [permissions.IsAdminUser]

#     def get(self, request, format=None):
#         """
#         Return a list of all users.
#        """
       
#        data=request.get()
#         usernames = [user.username for user in User.objects.all()]
#         return Response(usernames)

class StudentListView(generics.ListAPIView):
    queryset = student.objects.all()  # Ensure this line is present
    serializer_class = StudentSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]  # Ensure permission class is set
    
    
class MentorListView(generics.ListAPIView):
    queryset = mentor.objects.all()  # Ensure this line is present
    serializer_class = MentorSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]  # Ensure permission class is set

class StudentLogin(APIView):
    queryset = student.objects.all()  # Set your queryset here
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    """
    View to check if the student with given email and password exists in the system.
    """
    def get(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        
        if email is not None and password is not None:
            try:
                student_data = student.objects.filter(email=email).first()
                if student_data and student_data.password == password:
                    serializer = StudentSerializer(student_data)
                    return Response(serializer.data,status=status.HTTP_200_OK)
                else:
                    return Response({'status': 'error', 'message': 'Password is incorrect.'})
                # return Response({'status': 'success', 'message': 'Student exists.'})
            except student.DoesNotExist:
                return Response({'status': 'error', 'message': 'Student does not exist.'})
        else:
            return Response({'status': 'error', 'message': 'Email and password are required.'})
        
        
        
    def post(self, request, *args, **kwargs):
        pass
        serializer = StudentSerializer(data=request.data)
        if StudentSerializer.is_valid():
            StudentSerializer.save()
            return Response(StudentSerializer.data)
        else:
            return Response(StudentSerializer.errors)
        
        
        
        
        
class MentorLogin(APIView):
    queryset = mentor.objects.all()  # Set your queryset here
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    """
    View to check if the student with given email and password exists in the system.
    """
    def get(self, request, format=None):
        email = request.query_params.get('email', None)
        password = request.query_params.get('password', None)
        if email is not None and password is not None:
            try:
                mentor_data = mentor.objects.get(email=email, password=password)
                serializer=MentorSerializer(mentor_data)
                # return
                return Response(serializer.data,status=status.HTTP_200_OK)
                # return Response({'status': 'success', 'message': 'Student exists.'})
            except student.DoesNotExist:
                return Response({'status': 'error', 'message': 'Student does not exist.'})
        else:
            return Response({'status': 'error', 'message': 'Email and password are required.'})
        
        
    def post(self, request, format=None):
        serializer = MentorSerializer(data=request.data)
        if MentorSerializer.is_valid():
            MentorSerializer.save()
            return Response(MentorSerializer.data)
        else:
            return Response(MentorSerializer.errors)



