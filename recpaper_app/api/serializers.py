from rest_framework import serializers
from recpaper_app.models import User, Project, Project_log, Comment, Files


# class UserLoginSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Student
#         exclude=["password"]
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields  = "__all__"
        
# class MentorLoginSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Faculty
#         exclude=["password"]

class MentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields  = "__all__"
        



class ProjectSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    mentor = serializers.SerializerMethodField()
    p_user = serializers.SerializerMethodField()
    college = serializers.SerializerMethodField()
    
    def get_user(self,obj):
        return obj.user.username
    
    def get_mentor(self,obj):
        return obj.mentor.username
    
    def get_p_user(self,obj):
        return [obj.user.uuid,obj.mentor.uuid]
    def get_college(self,obj):
        return obj.user.college
    
    class Meta:
        model = Project
        fields = "__all__"
        

        

class ProjectLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project_log
        fields = "__all__"
        
        
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

class ProjectCreateSerializer(serializers.ModelSerializer):
    github_link = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    
    class Meta:
        model = Project
        fields = "__all__"
        
    

class FilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = "__all__"


