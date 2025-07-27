from django.db import models
import uuid
from recpaper_app.utils.blob_storage import VercelBlobStorage
import vercel_blob


class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class StudentManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.STUDENT)



class FacultyManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.FACULTY)


# use user for both studnet and mentor  type user
class User(BaseModel):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        STUDENT = "STUDENT", "Student"
        FACULTY = "FACULTY", "Faculty"
        
        
    username = models.CharField(max_length=50)
    mobile=models.CharField(max_length=20)
    user_id=models.CharField(max_length=50, unique=True)
    email=models.EmailField(max_length=50,unique=True)
    password=models.CharField(max_length=50)
    college=models.CharField(max_length=100)
    department=models.CharField(max_length=100)
    is_student = models.BooleanField(default=True)
    is_faculty = models.BooleanField(default=False)
    role = models.CharField(max_length=50, choices=Role.choices)
    active = models.BooleanField(default=True)
    verified_by_admin = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.username}"
    
    


class Student(User):
    role = User.Role.STUDENT
    object = StudentManager()
    
    class Meta:
        proxy = True

    def welcome(self):
        return "Only for students"
    
    


class Faculty(User):
    role = User.Role.FACULTY
    is_faculty=True
    is_student=False
    
    objects = FacultyManager()

    class Meta:
        proxy = True
        ordering=['username']

    def welcome(self):
        return "Only for students"
    
   
# # do not use mentor table
# class Mentor(BaseModel):
#     username = models.CharField(max_length=50)
#     mobile=models.CharField(max_length=20)
#     roll_no=models.CharField(max_length=50, unique=True)
#     email=models.EmailField(max_length=50,unique=True)
#     password=models.CharField(max_length=50)
#     college=models.CharField(max_length=100)
#     department=models.CharField(max_length=100)
#     is_faculty = models.BooleanField(default=True)
#     verified = models.BooleanField(default=False)
#     active = models.BooleanField(default=True)
    
#     def __str__(self):
#         return self.username
    

class Project(BaseModel):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="project_author")
    mentor=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="project_mentor")
    semester=models.IntegerField()
    title=models.CharField(max_length=500, unique=True)
    description=models.TextField()
    objective=models.TextField()
    status = models.CharField(max_length=500)
    keyword =models.TextField()
    platform =models.TextField()
    github_link = models.CharField(max_length=500, null=True)
    verified = models.BooleanField(default=False)
    public = models.BooleanField(default=False)
    group = models.BooleanField(default=False)
    collaboration = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    
    class Meta:
        ordering=['title']
        
        

class Groups(BaseModel):
    Project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="group_project")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="group_member")
    
    def __str__(self) -> str:
        return f"project :{self.Project.title} and member is: {self.user.username}"
    



class Project_log(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    mentor = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True)
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
    public = models.BooleanField(default=True)

    
    class Meta:
        verbose_name_plural = "Files"
        
        

    
    def __str__(self) -> str:
        return f"Title:{self.project.title} File:{self.message or 'No file Descriptions'}"

    def delete(self,*args, **kwargs):
        try:
            d = vercel_blob.delete(str(self.file))
            print(f"delete from vecel {self.file} response: {d}")
            super().delete(*args, **kwargs)
            print(f"File '{self.pk}' deleted successfully.")
            return True
        except Exception as e:
            print(f"Error deleting file '{self.pk}': {e}")
        

        

    