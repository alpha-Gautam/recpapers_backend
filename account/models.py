from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from .managers import StudentManager, FacultyManager,UserManager


# Create your models here.
class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True



class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        STUDENT = "STUDENT", "Student"
        FACULTY = "FACULTY", "Faculty"
        STAFF = "STAFF", "Staff"


    username = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    # middle_name = models.CharField(max_length=50, blank=True, default=None)
    last_name = models.CharField(max_length=50)

    mobile=models.CharField(max_length=20)
    user_id=models.CharField(max_length=50, unique=True)
    email=models.EmailField(max_length=50,unique=True)
    college=models.CharField(max_length=100)
    department=models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    is_student = models.BooleanField(default=True)
    is_faculty = models.BooleanField(default=False)
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.STUDENT)
    is_active = models.BooleanField(default=True)
    is_staff  = models.BooleanField(default=False)
    verified_by_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "mobile"]
    
    objects = UserManager()

    def __str__(self):
        return f"{self.username}"
    
    def get_full_name(self):
        # if self.middle_name:
        #     return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"



class Student(User):
    objects = StudentManager()
    
    class Meta:
        proxy = True

    def welcome(self):
        return "Only for students"
    
    


class Faculty(User):

    objects = FacultyManager()

    class Meta:
        proxy = True
        ordering=['username']

    def welcome(self):
        return "Only for faculty"
    
   