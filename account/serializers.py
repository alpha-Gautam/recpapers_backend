from rest_framework import serializers
from account.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'confirm_password', 'password')
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
        user = User.objects.create_student(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        user.is_active = False
        user.save()

        return user
    
    
    def update(self, instance, validated_data):
        # instance.email = validated_data.get('email', instance.email)
        # instance.first_name = validated_data.get('first_name', instance.first_name)
        # instance.last_name = validated_data.get('last_name', instance.last_name)
        oldusername=User.objects.get(username=validated_data['username'])
        if oldusername:
            raise serializers.ValidationError("Username already exists.")
        instance.username = validated_data.get('username', instance.username)

        # if 'password' in validated_data:
        #     instance.set_password(validated_data['password'])
        
        instance.save()
        return instance
    
