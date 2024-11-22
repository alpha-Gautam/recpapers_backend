from django.db import models

# Create your models here.

class student(models.Model):
    name=models.CharField(max_length=50)
    rollNum=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    college=models.CharField(max_length=50)
    branch=models.CharField(max_length=50)
    
    
    def __str__(self):
        return self.name

    
class mentor(models.Model):
    name=models.CharField(max_length=50)
    collegeId=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    college=models.CharField(max_length=50)
    department=models.CharField(max_length=50)
    
    
    def __str__(self):
        return self.name
