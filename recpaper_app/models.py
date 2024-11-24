from django.db import models

# Create your models here.
class User(models.Model):
    name=models.CharField(max_length=50)
    roll_no=models.CharField(max_length=50)
    email=models.EmailField(max_length=50,unique=True)
    password=models.CharField(max_length=50)
    college=models.CharField(max_length=50)
    branch=models.CharField(max_length=50)
    designation=models.CharField(max_length=50)
    
    
    def __str__(self):
        return self.name


class Paper(models.Model):
    title=models.CharField(max_length=50)
    objective=models.CharField(max_length=500)
    platform=models.CharField(max_length=100)
    description=models.CharField(max_length=200)
    # user=models.ForeignKey(User,on_delete=models.CASCADE)
    user=models.CharField(max_length=50)
    mentor=models.CharField(max_length=50)
    
    def __str__(self):
        return self.title
