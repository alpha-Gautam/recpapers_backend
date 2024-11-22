from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from .models import student,mentor
from .serializers import StudentSerializer, MentorSerializer
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


class StudentLogin(APIView):
    """
    View to check if the student with given email and password exists in the system.
    """
    def get(self, request, format=None):
        email = request.query_params.get('email', None)
        password = request.query_params.get('password', None)
        if email is not None and password is not None:
            try:
                student_data = student.objects.get(email=email, password=password)
                serializer=StudentSerializer(student_data)
                # return
                return Response(serializer.data)
                # return Response({'status': 'success', 'message': 'Student exists.'})
            except student.DoesNotExist:
                return Response({'status': 'error', 'message': 'Student does not exist.'})
        else:
            return Response({'status': 'error', 'message': 'Email and password are required.'})
        
        
        
    def post(self, request, format=None):
        email = request.query_params.get('email', None)
        password = request.query_params.get('password', None)
        if email is not None and password is not None:
            try:
                student_data = student.objects.get(email=email)
                # serializer=StudentSerializer(student_data)
                # return
                # return Response(serializer.data)
                return Response({'status': 'eroror', 'message': 'This email id is already exists.'})
            except student.DoesNotExist:
                
                return Response({'status': 'error', 'message': 'Student does not exist.'})
        else:
            return Response({'status': 'error', 'message': 'Email and password are required.'})
        
        
class MentorLogin(APIView):
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
                return Response(serializer.data)
                # return Response({'status': 'success', 'message': 'Student exists.'})
            except student.DoesNotExist:
                return Response({'status': 'error', 'message': 'Student does not exist.'})
        else:
            return Response({'status': 'error', 'message': 'Email and password are required.'})



