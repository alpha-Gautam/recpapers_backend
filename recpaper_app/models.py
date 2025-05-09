from django.db import models
import uuid
from recpaper_app.utils.blob_storage import VercelBlobStorage


class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True



class Mentor(BaseModel):
    username = models.CharField(max_length=50)
    mobile=models.CharField(max_length=20)
    roll_no=models.CharField(max_length=50, unique=True)
    email=models.EmailField(max_length=50,unique=True)
    password=models.CharField(max_length=50)
    college=models.CharField(max_length=100)
    department=models.CharField(max_length=100)
    is_faculty = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.username
    


class User(BaseModel):
    username = models.CharField(max_length=50)
    mobile=models.CharField(max_length=20)
    roll_no=models.CharField(max_length=50, unique=True)
    email=models.EmailField(max_length=50,unique=True)
    password=models.CharField(max_length=50)
    college=models.CharField(max_length=100)
    department=models.CharField(max_length=100)
    is_student = models.BooleanField(default=True)
    is_faculty = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.username
    
   

class Project(BaseModel):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="project_author")
    mentor=models.ForeignKey(Mentor, on_delete=models.SET_NULL, null=True, related_name="project_mentor")
    title=models.CharField(max_length=500, unique=True)
    description=models.TextField()
    objective=models.TextField()
    status = models.CharField(max_length=500)
    keyword =models.TextField()
    platform =models.TextField()
    github_link = models.CharField(max_length=500)
    verified = models.BooleanField(default=False)
    public = models.BooleanField(default=False)
    
  
    def __str__(self):
        return self.title
    
    
    class Meta:
        ordering=['title']





class Project_log(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    mentor = models.ForeignKey(Mentor, on_delete=models.SET_NULL, null=True)
    remark_by_mentor = models.TextField()
    current_status = models.TextField(null=True)
    verified = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.remark_by_mentor
    
    
class Comment(BaseModel):
    user = models.ForeignKey(User, models.CASCADE, related_name="comment_writer")
    project_uuid = models.ForeignKey(Project, models.CASCADE)
    message = models.TextField()
    
    
    def __str__(self) -> str:
        return self.message
    
    
class Files(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    file = models.FileField(storage=VercelBlobStorage(), upload_to='project_files', max_length=500)
    message = models.TextField(blank=True, null=True)

    
    class Meta:
        verbose_name_plural = "Files"

    
    def __str__(self) -> str:
        return self.message