from rest_framework.response import Response
from rest_framework.decorators import api_view, APIView
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from recpaper_app.models import User,Project, Keyword, UserLogin
from recpaper_app.api.serializers import UserSerializer,ProjectSerializer,KeywordSerializer, UserLoginSerializer
from rest_framework import status, authentication, permissions
from rest_framework import generics

@api_view(["GET","POST","PUT","PATCH", "DELETE"])    
def user_login(request,pk):
    if request.method == "GET":
        data= request.data
        if(data["email"] and data["password"]):
            if (UserLogin.objects.filter(email=data["email"])):
                return Response(status=200)
            else:
                return Response(status=400)
        else:
            return Response(status==400)
        
            
            
        # papers = User.objects.filter(email=pk)
        # serializer = UserSerializer(papers,many=True)
        # return Response(serializer.data)
    elif request.method == "POST":
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
        
@api_view(["GET","POST","PUT","PATCH", "DELETE"])    
def user_view(request):
    if request.method == "GET":
        papers = User.objects.all()
        serializer = UserSerializer(papers,many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
        
@api_view(["GET","POST","PUT","PATCH", "DELETE"])    
def keyword_view(request):
    if request.method == "GET":
        papers = Keyword.objects.all()
        serializer = KeywordSerializer(papers,many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = KeywordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    
    
@api_view(["GET","POST","PUT","PATCH", "DELETE"])
def project_view(request):
    if request.method == "GET":
        papers = Project.objects.all()
        serializer = ProjectSerializer(papers,many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    elif request.method == "DELETE":
        project_id = request.data.get('id')
        if not project_id:
            return Response({"error": "Project ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            project = Project.objects.get(id=project_id)
            project.delete()
            return Response({"message": "Project deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
    # if request.method == "PUT":
    #     serializer = ProjectSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     else:
    #         return Response(serializer.errors)
        
        
    
@api_view(["GET","POST","PUT","PATCH", "DELETE"])
def project_detail(request, pk):
    if request.method == "GET":
        papers = Project.objects.filter(project_uuid=pk)
        if not papers.exists():
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectSerializer(papers.first())
        return Response(serializer.data)
    # elif request.method == "POST":
    #     serializer = ProjectSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     else:
    #         return Response(serializer.errors)
        
    elif request.method == "DELETE":
        # project_uuid = request.data.get('id')
        if not pk:
            return Response({"error": "Project ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            project = Project.objects.filter(project_uuid=pk)
            project.delete()
            return Response({"message": "Project deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
    # if request.method == "PUT":
    #     serializer = ProjectSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     else:
    #         return Response(serializer.errors)
        
        
