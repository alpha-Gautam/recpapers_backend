from rest_framework import serializers
from chat_app.models import Messages



class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()
    receiver = serializers.SerializerMethodField()
    
    def get_sender(self,obj):
        return obj.sender.username
    def get_receiver(self,obj):
        return obj.receiver.username
    
    class Meta:
        model=Messages
        fields = "__all__"
        
