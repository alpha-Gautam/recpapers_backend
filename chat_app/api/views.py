from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, APIView


from chat_app.models import Messages


from chat_app.api.serializers import MessageSerializer




class messagesView(APIView):
    
    def get(self,request):
        queryset = Messages.objects.all()
        
        serializer = MessageSerializer(queryset, many=True)
        return Response({"message":"All messages",
                         "data":serializer.data},status=200)
        
    def post(self,request):
        
        data = request.data
        try:
            serializer = MessageSerializer(data)
            if(serializer.is_valid()):
                serializer.save()
                return Response({
                    "message":"data save successful",
                    "data":serializer.data
                },status=200)
            else:
                return Response({
                    "message":"data is not save",
                    "error":serializer.error_messages
                },status=400)
            
        except Exception as e:
            
            return Response({
                    "message":"something went wrong",
                    "error":str(e)
                },status=400)

    
class deleteMessage(APIView):
    def delete(self,request,pk):
        if not pk:
            return Response({"error": "Project UUID is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            message = Messages.objects.filter(uuid=pk)
            message.delete()
            return Response({"message": "message deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except message.DoesNotExist:
            return Response({"error": "message not found"}, status=status.HTTP_404_NOT_FOUND)
        