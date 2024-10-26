from rest_framework import serializers
from recpaper_app.models import User,Paper


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    roll_no = serializers.CharField()
    email = serializers.CharField()
    college = serializers.CharField()
    branch = serializers.CharField()
    designation = serializers.CharField()
    
    # this will create a new user object in database and return it
    def create(self, validated_data):
        return User.objects.create(**validated_data)
    
    # This will update the user object in database and return updated object
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.roll_no = validated_data.get('roll_no',instance.roll_no)
        instance.email = validated_data.get('email',instance.email)
        instance.college = validated_data.get('college',instance.college)
        instance.branch = validated_data.get('branch',instance.branch)
        instance.designation = validated_data.get('designation',instance.designation)
        instance.save()
        return instance

class PaperSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    objective = serializers.CharField()
    platform = serializers.CharField()
    description = serializers.CharField()

    def create(self, validated_data):
        return Paper.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title',instance.title)
        instance.objective = validated_data.get('objective',instance.objective)
        instance.platform = validated_data.get('platform',instance.platform)
        instance.description = validated_data.get('description',instance.description)
        instance.save()
        return instance

