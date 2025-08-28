import uuid
from rest_framework import serializers
from account.models import User


class UserSerializer(serializers.ModelSerializer):
   
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    username = serializers.CharField(required=False)
    user_id = serializers.CharField(required=False)
    class Meta:
        model = User
        fields = "__all__"
        # fields = ('email', 'username', 'first_name', 'last_name', 'confirm_password', 'password',"role")
        # read_only_fields = ('id', 'is_active', 'is_admin', 'is_superuser')

    
    def validate(self, attrs):
        if attrs.get("password") != attrs.get("confirm_password"):
            raise serializers.ValidationError("Passwords and confirm passwords do not match.")
        return attrs
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value
    
    def create(self, validated_data):
        validated_data.pop("confirm_password", None)
        suffix=str(uuid.uuid4())[:8]
        if "user_id" not in validated_data:
            validated_data["user_id"] = validated_data["first_name"] + "_" + suffix
        if "username" not in validated_data or not validated_data["username"]:
            validated_data["username"] = validated_data["first_name"] + "_" + suffix

        user = User.objects.create_student(
            **validated_data
        )
        user.save()

        return user
    
    
    def update(self, instance, validated_data):
        # instance.first_name = validated_data.get('first_name', instance.first_name)
        # instance.last_name = validated_data.get('last_name', instance.last_name)
        if validated_data.get("username"):
            newusername=User.objects.get(username=validated_data['username'])
            if newusername:
                raise serializers.ValidationError("Username already exists.")
            instance.username = validated_data.get('username', instance.username)

          
        instance.save()
        return instance
    
