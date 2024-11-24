from django.db import models

# Create your models here.

class student(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name=models.CharField(max_length=50)
    rollNum=models.IntegerField(unique=True)
    email=models.EmailField(max_length=50,unique=True)
    password=models.CharField(max_length=50)
    college=models.CharField(max_length=50)
    branch=models.CharField(max_length=50)
    
    
    def __str__(self):
        return self.name
    
    # # this is for order the objects by created values
    # class Meta:
    #     ordering = ['created']

    
class mentor(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name=models.CharField(max_length=50)
    collegeId=models.IntegerField(unique=True)
    email=models.EmailField(max_length=50,unique=True)
    password=models.CharField(max_length=50)
    college=models.CharField(max_length=50)
    department=models.CharField(max_length=50)
    
    
    def __str__(self):
        return self.name
