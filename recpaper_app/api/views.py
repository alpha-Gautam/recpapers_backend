from rest_framework.response import Response
from rest_framework.decorators import api_view, APIView
from recpaper_app.models import Student, Faculty, Project, Project_log, Comment, Files
from recpaper_app.api.serializers import (UserSerializer, MentorSerializer, MentorLoginSerializer,
                                          ProjectSerializer, UserLoginSerializer, ProjectLogSerializer, 
                                          CommentSerializer, ProjectCreateSerializer, MentorCreateSerializer, 
                                          FilesSerializer)
from rest_framework import status, authentication, permissions
from  django.db.models import Q
from recpaper_app.utils.blob_storage import upload_to_blob, delete_from_blob
# ["GET","POST","PUT","PATCH", "DELETE"]



class user_login(APIView):
    def post(self, request):
        data = request.data
        print("api data for user login ->",data)
        # Check if email and password are provided
        if("email" in data and "password" in data):
            
        #==================Student Login Login===================\
            
            if("role" in data and data["role"]=="Student"):
                userData = Student.objects.filter(email=data["email"]).first()  # Use first() to get a single user
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
                mentorData = Faculty.objects.filter(email=data["email"]).first()  # Use first() to get a single user
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
        data=request.data
        try:
            if(data["is_student"]==True and data["is_faculty"]==False):
                data["role"]="STUDENT"
                
                serializer = UserSerializer(data=data)
                # print("data for user ragristration--->",data)
                print("afer serialize data for user ragristration--->",serializer)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors,status=400)
                
            elif(data["is_student"]==False and data["is_faculty"]==True):
                data["role"]="FACULTY"

                serializer = MentorCreateSerializer(data=data)
                print("data for user ragristration--->",data)
                print("afer serialize data for user ragristration--->",serializer)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors,status=400)
                
                
        except Exception as e:
            print("Error during ragister:- ",e)
            return Response({"message":"something went wrong"},status=400)
            
        
class user_view(APIView):
    
    def get(self, request):
        user_data = Student.objects.all()
        serializer = UserSerializer(user_data,many=True)
        return Response(serializer.data)
    
class mentor_view(APIView):
    def get(self, request):
        mentor=Faculty.objects.all()
        serializer = MentorSerializer(mentor ,many=True)
        return Response(serializer.data)
         
         
class User_project_view(APIView):
    def get(self,request):
        # user = request.user
        data=request.data
        print("user_data-->",data)
        # print("user_-->",user)
        try:
            queryset = Project.objects.filter(Q(user__iexact=data["user_id"])|Q(mentor__iexact=data["user_id"]))
            return Response(
                {"message":"user project",
                 "data":queryset},
                status=200
            )
            
        except Exception as e:
            return Response({"message":"something went wrong","error":str(e)},status=400)
            
            
    
class project_view(APIView):
    
    def get(self, request):
        try:
            queryset = Project.objects.all()

            if(request.GET.get("search")):
                search = request.GET.get("search")
                queryset=queryset.filter(
                    Q(title__icontains=search)|
                    Q(user__username__icontains=search)|
                    Q(mentor__username__icontains=search)|
                    Q(platform__icontains=search)|
                    Q(keyword__icontains=search)
                )


            serializer = ProjectSerializer(queryset,many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(data=e,status=400)
    
    # def post(self, request):
    #     try:
    #         data = request.data
    #         serializer = ProjectSerializer(data=data)  # Fixed: using data keyword
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data, status=200)
    #         else:
    #             return Response({"message":"fill the valid data"}, status=400)  
    #     except Exception as e:
    #         return Response({"message": str(e)}, status=400)  # Fixed: converting exception to string
        
        
        
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
        papers = Project.objects.filter(uuid=pk)
        if not papers.exists():
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectSerializer(papers.first())
        return Response(serializer.data)
    
    
    def delete(self, request,pk):
        if not pk:
            return Response({"error": "Project UUID is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            project = Project.objects.filter(project_uuid=pk)
            project.delete()
            return Response({"message": "Project deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
        
   
        
class project_create(APIView):
    def post(self, request):
        try:
            data = request.data
            print("project data:", data)
            serializer = ProjectCreateSerializer(data=data)  # Fixed: properly passing data parameter
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            else:
                return Response({
                    "message": "Validation failed",
                    "errors": serializer.errors
                }, status=400)  
        except Exception as e:
            return Response({
                "message": "Something went wrong",
                "error": str(e)
            }, status=400)
    
    def patch(self, request):
        try:
            data = request.data
            if "uuid" not in data:
                return Response({"message": "Project UUID is required"}, status=400)
            
            project_object, created = Project.objects.get_or_create(uuid=data.get("uuid"))
            if created:
                return Response({"message": "Invalid project UUID"}, status=400)
            
            serializer = ProjectCreateSerializer(project_object, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Project updated!","data":serializer.data}, status=200)
            else:
                return Response({"message": "Data is not valid", "error": str(serializer.errors)}, status=400)
        except Exception as e:
            return Response({"message": "Something went wrong", "error": str(e)}, status=400)
        
 
 
class verify_project(APIView):
    # authentication_classes = [authentication.SessionAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        data=request.data
        # if not pk:
        #     return Response({"message": "Project ID is required"}, status=400)
        print("data project:--",data)
        try:
            # Get the faculty user
            user = Faculty.objects.filter(uuid=data["user"]).first()
            if not user:
                return Response({"message": "User not found or not a faculty member"}, status=404)
            
            # Check if faculty is verified by admin
            if not user.verified_by_admin:
                return Response({"message": "Mentor is not authenticated by admin"}, status=403)
            
            # Get and verify project
            project = Project.objects.filter(uuid=data["project"]).first()
            if not project:
                return Response({"message": "Project not found"}, status=404)
            
            # Check if the requesting user is the mentor
            if project.mentor and project.mentor.uuid != user.uuid:
                return Response({"message": "Only the assigned project mentor can verify the project"}, status=403)
            
            # Update the project verification status
            project.verified = not project.verified
            project.save()
            
            serializer = ProjectCreateSerializer(project)
            return Response({
                "message": "Project verified successfully",
                "data": serializer.data
            }, status=200)
                
        except Exception as e:
            return Response({
                "message": "Something went wrong",
                "error": str(e)
            }, status=400)
                
            
            
        
            
        
class porject_log(APIView):
    
    def get(self, request, pk):
 
        try:
            log = Project_log.objects.filter(project=pk)
            serializer=ProjectLogSerializer(log,many=True)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        except Project_log.DoesNotExist:
            return Response({"error": "Project log not found"}, status=status.HTTP_404_NOT_FOUND)
            
    def post(self, request):        
        data=request.data
        serializer = ProjectLogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
   
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
        serializer = CommentSerializer(data=data)  # Fixed: properly passing data parameter
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    
class file_upload(APIView):
    def get(self, request, pk):
        try:
            queryset = Files.objects.filter(project=pk)
            serializer = FilesSerializer(queryset, many=True)
            return Response(serializer.data, status=200)
        
        except Exception as e:
            return Response({"error": str(e)}, status=500)
            
    def post(self, request, pk):
        try:
            # Verify project exists
            project = Project.objects.get(uuid=pk)
            if project==None:
                return Response({"message":"Invalid project id"},status=400)
            # Get file and message
            file_obj = request.FILES.get('file')
            if not file_obj:
                return Response({"error": "No file provided"}, status=400)
            message = request.data.get('message', '')
            
            # Create file record - storage backend handles upload to Vercel Blob
            file_instance = Files.objects.create(
                project=project,
                file=file_obj,
                message=message
            )
            
            serializer = FilesSerializer(file_instance)
            return Response(serializer.data, status=201)
            
        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
    
    def delete(self, request, pk):
        try:
            # file_uuid = request.query_params.get('file_uuid') or request.data.get('file_uuid')
            # if not file_uuid:
            #     return Response({"error": "File UUID required"}, status=400)
            
            # Get and delete file - storage backend handles deletion from Blob
            file_instance = Files.objects.get(uuid=pk)
            re=file_instance.delete()
            if re==False:
                return Response({"message":"deletion Failed !"}, status=400)
                
            
            return Response({"message": "File deleted successfully"}, status=200)
            
        except Files.DoesNotExist:
            return Response({"error": "File not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
