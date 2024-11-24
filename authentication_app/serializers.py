from rest_framework import serializers
from .models import student,mentor


class StudentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    name = serializers.CharField()
    rollNum = serializers.IntegerField()
    email = serializers.EmailField()
    password=serializers.CharField(write_only=True)
    college = serializers.CharField()
    branch = serializers.CharField()
        
    
    def validate_rollNum(self, value):
       # Check if the rollNum already exists
       if student.objects.filter(rollNum=value).exists():
           raise serializers.ValidationError("This Roll-Num is already exists.")
       return value
    def validate_email(self, value):
       # Check if the email already exists
       if student.objects.filter(email=value).exists():
           raise serializers.ValidationError("This email is already exists.")
       return value

    # this will create a new user object in database and return it
    def create(self, validated_data):
        return student.objects.create(**validated_data)



class MentorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    name = serializers.CharField()
    collegeId = serializers.IntegerField()
    email = serializers.EmailField()
    password=serializers.CharField(write_only=True)
    college = serializers.CharField()
    department = serializers.CharField()
    
    
    def validate_collegeId(self, value):
       # Check if the collegeId already exists
       if mentor.objects.filter(collegeId=value).exists():
           raise serializers.ValidationError("This college-Id is already exists.")
       return value
    def validate_email(self, value):
       # Check if the email already exists
       if mentor.objects.filter(email=value).exists():
           raise serializers.ValidationError("This email is already exists.")
       return value
    
    # this will create a new user object in database and return it
    def create(self, validated_data):
        return mentor.objects.create(**validated_data)