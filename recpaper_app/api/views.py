from rest_framework.response import Response
from rest_framework.decorators import api_view, APIView
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from recpaper_app.models import User, Mentor, Project, Project_log, Comment, Platform
from recpaper_app.api.serializers import UserSerializer, MentorSerializer, MentorLoginSerializer, ProjectSerializer, UserLoginSerializer, ProjectLogSerializer,CommentSerializer, PlatformSerializer
from rest_framework import status, authentication, permissions
from rest_framework import generics


# ["GET","POST","PUT","PATCH", "DELETE"]



class user_login(APIView):
    def post(self, request):
    # if request.method == "POST":
        data = request.data
        print("api data for user login ->",data)
        # Check if email and password are provided
        if "email" in data and "password" in data:
            
        #==================Student Login Login===================\
            
            if("role" in data and data["role"]=="Student"):
                userData = User.objects.filter(email=data["email"]).first()  # Use first() to get a single user
                if userData:
                    if userData.password == data["password"]:  # Compare password
                        serializer=UserLoginSerializer(userData)
                        return Response(data=serializer.data, status=200)
                    else:
                        return Response({"message": "Password is incorrect!"}, status=401)
                else:
                    return Response({"message": "User not found! Enter rignt email"}, status=404)

        #==================Mentor Login Login===================
        
        
            elif("role" in data and  data["role"]=="Mentor"):
                mentorData = Mentor.objects.filter(email=data["email"]).first()  # Use first() to get a single user
                if mentorData:
                    if mentorData.password == data["password"]:  # Compare password
                        serializer=MentorLoginSerializer(mentorData)
                        return Response(data=serializer.data, status=200)
                    else:
                        return Response({"message": "Password is incorrect!"}, status=401)
                else:
                    return Response({"message": "User not found! Enter rignt email"}, status=404)
                    
            else:
                return Response({
                    "status":False,
                    "message" : "Some thing went worng please try againg"
                },status=400)
        else:
            return Response({"message": "Email and password are required!"}, status=400)
            
            
        # papers = User.objects.filter(email=pk)
        # serializer = UserSerializer(papers,many=True)
        # return Response(serializer.data)
 
 

class user_ragister(APIView):
    def post(self, request):
    # if request.method == "POST":
        data=request.data
        try:
            if(data["is_student"]==True and data["is_faculty"]==False):

                serializer = UserSerializer(data=data)
                print("data for user ragristration--->",data)
                print("afer serialize data for user ragristration--->",serializer)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors,status=400)
                
            elif(data["is_student"]==False and data["is_faculty"]==True):

                serializer = MentorSerializer(data=data)
                print("data for user ragristration--->",data)
                print("afer serialize data for user ragristration--->",serializer)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors,status=400)
                
                
        except Exception as e:
            print("Error during ragister:- ",e)
            return Response({
                
                "message":"something went wrong",
                
            },status=400)
            
        
class user_view(APIView):
    
    def get(self, request):
        user_data = User.objects.all()
        serializer = UserSerializer(user_data,many=True)
        return Response(serializer.data)
    
class mentor_view(APIView):
    def get(self, request):
        mentor=Mentor.objects.all()
        serializer = MentorSerializer(mentor ,many=True)
        return Response(serializer.data)
        
        
class platform_view(APIView):
    def get(self, request):
        platform = Platform.objects.all()
        serializer = PlatformSerializer(platform, many=True)
        return Response(serializer.data,status=200)
    
    
    
class project_view(APIView):
    
    def get(self, request):
    # if request.method == "GET":
        papers = Project.objects.all()
        serializer = ProjectSerializer(papers,many=True)
        return Response(serializer.data)
    
    
    def post(self, request):
    # elif request.method == "POST":
        data=request.data
        print("project data :- ", data)
        serializer = ProjectSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
        
        
    def delete(self, request):
    # elif request.method == "DELETE":
        project_id = request.data.get('id')
        if not project_id:
            return Response({"error": "Project ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            project = Project.objects.get(id=project_id)
            project.delete()
            return Response({"message": "Project deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
    
    # def put(self, request):
    # if request.method == "PUT":
    #     serializer = ProjectSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     else:
    #         return Response(serializer.errors)
        
        
    
class project_detail(APIView):
    def get(self,request,pk):
    # if request.method == "GET":
        papers = Project.objects.filter(uuid=pk)
        if not papers.exists():
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectSerializer(papers.first())
        return Response(serializer.data)
    
    
    def delete(self, request,pk):
    # elif request.method == "DELETE":
        if not pk:
            return Response({"error": "Project UUID is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            project = Project.objects.filter(project_uuid=pk)
            project.delete()
            return Response({"message": "Project deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
        
        
    def put(self, request, pk):
    # if request.method == "PUT":
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
        
        
# @api_view(["GET","POST"])
class porject_log(APIView):
    
    def get(self, request, pk):
 
            try:
                log = Project_log.objects.filter(project=pk)
                serializer=ProjectLogSerializer(log,many=True)
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            except Project_log.DoesNotExist:
                return Response({"error": "Project log not found"}, status=status.HTTP_404_NOT_FOUND)
            
    def post(self, request, pk):        
        data=request.data
        serializer = ProjectLogSerializer(data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        
# @api_view(["GET","POST"])
class Project_comments(APIView):
    
    def get(self, request):
    # if request.methode=="GET":
        data=request.data
        if "project_uuid" in data:
            try:
                log = Comment.objects.filter(project_uuid=data["project_uuid"])
                return Response(log, status=status.HTTP_202_ACCEPTED)
            except Project_log.DoesNotExist:
                return Response({"error": "Project log not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):            
    # if request.methode=="POST":
        data=request.data
        serializer = CommentSerializer(data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        