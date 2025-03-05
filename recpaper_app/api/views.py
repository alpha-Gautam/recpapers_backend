from rest_framework.response import Response
from rest_framework.decorators import api_view, APIView
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from recpaper_app.models import User, Project, Keyword, Project_log, Comment
from recpaper_app.api.serializers import UserSerializer,ProjectSerializer,KeywordSerializer, UserLoginSerializer, UserLoginSerializer, ProjectLogSerializer,CommentSerializer
from rest_framework import status, authentication, permissions
from rest_framework import generics


# ["GET","POST","PUT","PATCH", "DELETE"]


@api_view(["POST"])
def user_login(request):
    if request.method == "POST":
        data = request.data
        print("api data ->",data)
        # Check if email and password are provided
        if "email" in data and "password" in data:
            userData = User.objects.filter(email=data["email"]).first()  # Use first() to get a single user
            if userData:
                if userData.password == data["password"]:  # Compare password
                    serializer=UserLoginSerializer(userData)
                    return Response(data=serializer.data, status=200)
                else:
                    return Response({"message": "Password is incorrect!"}, status=401)
            else:
                return Response({"message": "User not found! Enter rignt email"}, status=404)
        else:
            return Response({"message": "Email and password are required!"}, status=400)
            
            
        # papers = User.objects.filter(email=pk)
        # serializer = UserSerializer(papers,many=True)
        # return Response(serializer.data)
 
 
@api_view(["POST"])
def user_ragister(request):
    if request.method == "POST":
        data=request.data
        serializer = UserSerializer(data=data)
        print("data for user ragristration--->",data)
        print("afer serialize data for user ragristration--->",serializer)
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
        data=request.data
        print("project data :- ", data)
        serializer = ProjectSerializer(data=data)
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
        papers = Project.objects.filter(id=pk)
        if not papers.exists():
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectSerializer(papers.first())
        return Response(serializer.data)        
    elif request.method == "DELETE":
        if not pk:
            return Response({"error": "Project UUID is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            project = Project.objects.filter(project_uuid=pk)
            project.delete()
            return Response({"message": "Project deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
        
    if request.method == "PUT":
        try:
            project = Project.objects.get(project_uuid=pk)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
@api_view(["GET","POST"])
def porject_log(request):
    if request.methode=="GET":
        data=request.data
        if "project_uuid" in data:
            try:
                log = Project_log.objects.filter(project_uuid=data["project_uuid"])
                return Response(log, status=status.HTTP_202_ACCEPTED)
            except Project_log.DoesNotExist:
                return Response({"error": "Project log not found"}, status=status.HTTP_404_NOT_FOUND)
    if request.methode=="POST":
        data=request.data
        serializer = ProjectLogSerializer(data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        
@api_view(["GET","POST"])
def Project_comments(request):
    if request.methode=="GET":
        data=request.data
        if "project_uuid" in data:
            try:
                log = Comment.objects.filter(project_uuid=data["project_uuid"])
                return Response(log, status=status.HTTP_202_ACCEPTED)
            except Project_log.DoesNotExist:
                return Response({"error": "Project log not found"}, status=status.HTTP_404_NOT_FOUND)
    if request.methode=="POST":
        data=request.data
        serializer = CommentSerializer(data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        