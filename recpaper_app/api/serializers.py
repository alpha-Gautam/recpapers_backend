from rest_framework import serializers
from recpaper_app.models import User, Project, Keyword, UserLogin



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields  = "__all__"

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLogin
        fields  = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        # fields = ['id', 'title', 'code', 'linenos', 'language', 'style']
        fields = "__all__"
        
        
class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        # fields = ['id', 'title', 'code', 'linenos', 'language', 'style']
        fields = "__all__"









# class UserSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField()
#     roll_no = serializers.CharField()
#     email = serializers.EmailField()
#     password=serializers.CharField(write_only=True)
#     college = serializers.CharField()
#     branch = serializers.CharField()
#     designation = serializers.CharField()
    
#     def validate_email(self, value):
#        # Check if the email already exists
#        if User.objects.filter(email=value).exists():
#            raise serializers.ValidationError("This email is already exists.")
#        return value
    
#     # this will create a new user object in database and return it
#     def create(self, validated_data):
#         return User.objects.create(**validated_data)
    
#     # This will update the user object in database and return updated object
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name',instance.name)
#         instance.roll_no = validated_data.get('roll_no',instance.roll_no)
#         instance.email = validated_data.get('email',instance.email)
#         instance.college = validated_data.get('college',instance.college)
#         instance.branch = validated_data.get('branch',instance.branch)
#         instance.designation = validated_data.get('designation',instance.designation)
#         instance.save()
#         return instance

class projectSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    objective = serializers.CharField()
    platform = serializers.CharField()
    description = serializers.CharField()
    user=serializers.CharField()
    mentor=serializers.CharField()
    
    # title=models.CharField(max_length=50)
    # objective=models.CharField(max_length=500)
    # platform=models.CharField(max_length=100)
    # description=models.CharField(max_length=200)
    # user=models.ForeignKey(User,on_delete=models.CASCADE)
    # mentor=models.CharField(max_length=50)
    
    

    def create(self, validated_data):
        return Paper.objects.create(**validated_data)
    
    # def update(self, instance, validated_data):
    #     instance.title = validated_data.get('title',instance.title)
    #     instance.objective = validated_data.get('objective',instance.objective)
    #     instance.platform = validated_data.get('platform',instance.platform)
    #     instance.description = validated_data.get('description',instance.description)
    #     instance.save()
    #     return instance

