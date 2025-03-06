from django.db import models


# class UserLogin(models.Model):
#     email=models.EmailField(max_length=50,unique=True)
#     password= models.CharField(max_length=50)
    
     


class User(models.Model):
    user_uuid =models.CharField(max_length=100,unique=True)   
    username = models.CharField(max_length=50)
    mobile=models.CharField(max_length=20)
    email=models.EmailField(max_length=50,unique=True)
    password=models.CharField(max_length=100)
    college=models.CharField(max_length=50)
    department=models.CharField(max_length=50)
    is_student = models.BooleanField(default=True)
    is_faculty = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username

class Project(models.Model):
    project_uuid = models.CharField(max_length=100,unique=True)    
    # user=models.ForeignKey(User,on_delete=models.CASCADE)
    # mentor=models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    user_uuid = models.CharField(max_length=100) 
    mentor_uuid = models.CharField(max_length=100) 
    title=models.CharField(max_length=500, unique=True)
    keyword =models.CharField(max_length=500)
    objective=models.CharField(max_length=1000)
    description=models.CharField(max_length=1000)
    status = models.CharField(max_length=500)
    github_link = models.CharField(max_length=500)
    verified = models.BooleanField(default=False) 
    created_at =  models.DateTimeField(auto_now_add=True)
    last_updated_at =  models.DateTimeField(auto_now=True)
    
    # def __str__(self):
    #     return self.title
    
    def __str__(self):
        return f"{self.title} (Project ID: {self.id})"



class Platform(models.Model):
    project_uuid = models.CharField(max_length=100)
    platform_name = models.TextField()
    
    def __str__(self) -> str:
        return self.name
    

    
class Keyword(models.Model):
    
    # project_id = models.ForeignKey('project', on_delete=models.CASCADE)
    project_uuid = models.CharField(max_length=100)
    name = models.TextField()
    
    def __str__(self) -> str:
        return self.name
    
    
class Project_log(models.Model):
    # project_uuid = models.ForeignKey('project', on_delete=models.CASCADE)
    user_uuid = models.CharField(max_length=100)
    project_uuid = models.CharField(max_length=100)
    remark_by_mentor = models.TextField()
    current_status = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    verified = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.project_uuid
    
    
class Comment(models.Model):
    user_uuid = models.CharField(max_length=100)
    project_uuid = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.name
    
    