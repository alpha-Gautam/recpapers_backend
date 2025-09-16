from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager


# Create your models here.
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True



class User(BaseModel, AbstractBaseUser):
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
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.STUDENT)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)   
    is_admin = models.BooleanField(default=False)
    verified_by_admin = models.BooleanField(default=False)

    # groups = models.ManyToManyField(
    #     Group,
    #     related_name='account_user_groups',  # Change this to something unique
    #     blank=True
    # )
    # user_permissions = models.ManyToManyField(
    #     Permission,
    #     related_name='account_user_permissions',  # Change this to something unique
    #     blank=True
    # )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "mobile"]

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"
    
    def get_full_name(self):
        # if self.middle_name:
        #     return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        
        return True
    
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True
    
    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     "All admins are staff."
    #     return self.role==User.Role.ADMIN




# class Student(User):
#     objects = StudentManager()
    
#     class Meta:
#         proxy = True

#     def welcome(self):
#         return "Only for students"
    
    


# class Faculty(User):

#     objects = FacultyManager()

#     class Meta:
#         proxy = True
#         ordering=['username']

#     def welcome(self):
#         return "Only for faculty"



# class Designation(BaseModel):
#     title = models.CharField(max_length=100)


#     def __str__(self):
#         return self.title
    
    
# class College(BaseModel):
#     name = models.CharField(max_length=100)
#     college_id = models.CharField(max_length=50, unique=True)
#     location = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name