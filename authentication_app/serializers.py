from rest_framework import serializers
from .models import student,mentor


class StudentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    rollNum = serializers.CharField()
    email = serializers.CharField()
    college = serializers.CharField()
    branch = serializers.CharField()
    
    # this will create a new user object in database and return it
    def create(self, validated_data):
        return student.objects.create(**validated_data)



class MentorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    collegeId = serializers.CharField()
    email = serializers.CharField()
    college = serializers.CharField()
    department = serializers.CharField()
    
    # this will create a new user object in database and return it
    def create(self, validated_data):
        return student.objects.create(**validated_data)