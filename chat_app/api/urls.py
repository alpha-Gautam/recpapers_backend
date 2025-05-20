from django.urls import path, include

from chat_app.api.views import messagesView,deleteMessage


# from django.conf import settings
# from django.conf.urls.static import static
 


urlpatterns = [
   
    path('all_messages/', messagesView.as_view(), name='all_messages'),
    
    path('deletemessage/<str:pk>', deleteMessage.as_view(), name="delete_message")
    
]
