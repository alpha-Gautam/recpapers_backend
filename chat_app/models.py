from django.db import models
from recpaper_app.models import User
import uuid
# from recpaper_app.utils.blob_storage import VercelBlobStorage
# import vercel_blob


class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        

class Messages(BaseModel):
    sender = models.ForeignKey(User,on_delete=models.CASCADE, related_name="message_sender")
    receiver = models.ForeignKey(User,on_delete=models.CASCADE, related_name="message_receiver")
    message = models.TextField()

