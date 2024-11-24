from rest_framework.response import Response
from rest_framework.decorators import api_view, APIView
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from recpaper_app.models import User,Paper
from recpaper_app.api.serializers import UserSerializer,PaperSerializer
from rest_framework import status
from rest_framework import generics

# User Views

class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    
class PaperListView(generics.ListCreateAPIView):
    queryset = Paper.objects.all()
    serializer_class = PaperSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    

@api_view(["GET","PUT","DELETE"])
def user_login(request):
    if request.method == "GET":
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        if email is not None and password is not None:
            try:
                user_data = User.objects.filter(email=email).first()
                if user_data and user_data.password == password:
                    serializer = UserSerializer(user_data)
                    return Response(serializer.data)
                else:
                    return Response({'status': 'error', 'message': 'Password is incorrect.'})
                # return Response({'status': 'success', 'message': 'Student exists.'})
            except:
                return Response({'status': 'error', 'message': 'Student does not exist.'})
        else:
            return Response({'status': 'error', 'message': 'Email and password are required.'})
        
    # if request.method == "PUT":
    #     user = User.objects.get(pk=pk)
    #     serializer = UserSerializer(user,data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     else:
    #         return Response(serializer.errors)
    # if request.method == "DELETE":
    #     user = User.objects.get(pk=pk)
    #     user.delete()
    #     return Response(user,status=status.HTTP_204_NO_CONTENT)
    
# @api_view(["GET","PUT","DELETE"])
# def user_detail(request, pk):
#     if request.method == "GET":
#         user = User.objects.get(pk=pk)
#         serializer = UserSerializer(user)
#         return Response(serializer.data)
#     if request.method == "PUT":
#         user = User.objects.get(pk=pk)
#         serializer = UserSerializer(user,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
#     if request.method == "DELETE":
#         user = User.objects.get(pk=pk)
#         user.delete()
#         return Response(user,status=status.HTTP_204_NO_CONTENT)
    
    
    
@api_view(["GET","POST"])
def paper_list(request):
    if request.method == "GET":
        papers = Paper.objects.all()
        serializer = PaperSerializer(papers,many=True)
        return Response(serializer.data)
    if request.method == "POST":
        serializer = PaperSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
        

@api_view(["GET","PUT","DELETE"])
def paper_detail(request, pk):
    if request.method == "GET":
        paper = Paper.objects.get(pk=pk)
        serializer = PaperSerializer(paper)
        return Response(serializer.data)
    if request.method == "PUT":
        paper = Paper.objects.get(pk=pk)
        serializer = PaperSerializer(paper,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    if request.method == "DELETE":
        paper = Paper.objects.get(pk=pk)
        paper.delete()
        return Response(paper,status=status.HTTP_204_NO_CONTENT)
