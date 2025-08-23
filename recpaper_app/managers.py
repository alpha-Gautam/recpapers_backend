from django.db import models
from django.contrib.auth.models import BaseUserManager

class StudentManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        # Import here to avoid circular import
        from .models import User
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.STUDENT)

class FacultyManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        # Import here to avoid circular import
        from .models import User
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.FACULTY)

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_student(self, email, username, mobile, college, department, password=None, **extra_fields):
        from .models import User  # Import here to avoid circular import
        extra_fields.setdefault('role', User.Role.STUDENT)
        extra_fields.setdefault('is_student', True)
        extra_fields.setdefault('is_faculty', False)
        
        user = self.model(
            email=email,
            username=username,
            mobile=mobile,
            college=college,
            department=department,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_faculty(self, email, username, mobile, college, department, password=None, **extra_fields):
        from .models import User  # Import here to avoid circular import
        extra_fields.setdefault('role', User.Role.FACULTY)
        extra_fields.setdefault('is_student', False)
        extra_fields.setdefault('is_faculty', True)
        
        user = self.model(
            email=email,
            username=username,
            mobile=mobile,
            college=college,
            department=department,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, username, mobile, college, department, password=None, **extra_fields):
        from .models import User  # Import here to avoid circular import
        extra_fields.setdefault('role', User.Role.STAFF)
        extra_fields.setdefault('is_staff', True)
        
        user = self.model(
            email=email,
            username=username,
            mobile=mobile,
            # college=college,
            # department=department,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, mobile, password=None, college=None, department=None, **extra_fields):
        from .models import User  # Import here to avoid circular import
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.Role.ADMIN)
        
        if college is not None:
            extra_fields['college'] = college
        else:
            extra_fields.setdefault('college', 'Admin College')
                        
        if department is not None:
            extra_fields['department'] = department
        else:
            extra_fields.setdefault('department', 'Admin Department')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password,
                                username=username,
                                mobile=mobile, 
                                **extra_fields)
