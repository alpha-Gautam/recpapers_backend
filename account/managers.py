import uuid
from django.db import models
from django.contrib.auth.models import BaseUserManager

# class StudentManager(models.Manager):
#     def get_queryset(self, *args, **kwargs):
#         # Import here to avoid circular import
#         from .models import User
#         results = super().get_queryset(*args, **kwargs)
#         return results.filter(role=User.Role.STUDENT)

# class FacultyManager(models.Manager):
#     def get_queryset(self, *args, **kwargs):
#         # Import here to avoid circular import
#         from .models import User
#         results = super().get_queryset(*args, **kwargs)
#         return results.filter(role=User.Role.FACULTY)

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        prefix = extra_fields.get("first_name", "user")
        suffix = str(uuid.uuid4())[:8]
        if "user_id" not in extra_fields:
            extra_fields["user_id"] = prefix + "_" + suffix
        if "username" not in extra_fields or not extra_fields["username"]:
            extra_fields["username"] = prefix + "_" + suffix

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_student(self, email, password=None, **extra_fields):
        from .models import User  # Import here to avoid circular import

        user = self.create_user(
            email=email,
            password=password,
            **extra_fields
        )
        user.role = User.Role.STUDENT
        user.is_active = False
        user.verified_by_admin = False
        user.save(using=self._db)
        return user

    def create_faculty(self, email, password=None, **extra_fields):
        from .models import User  # Import here to avoid circular import
       
        
        user = self.create_user(
            email=email,
            password=password,
            **extra_fields
        )
        user.role = User.Role.FACULTY
        user.is_active = False
        user.verified_by_admin = False
        user.save(using=self._db)
        return user

    def create_staff(self, email, password=None, **extra_fields):
        from .models import User  # Import here to avoid circular import
      
        user = self.create_user(
            email=email,           
            password=password,
            **extra_fields
        )
        user.role = User.Role.STAFF
        user.is_staff = True
        user.is_active = False
        user.verified_by_admin = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        from .models import User  # Import here to avoid circular import

        if 'college' not in extra_fields:
            extra_fields['college'] = 'Admin College'
        if 'department' not in extra_fields:
            extra_fields['department'] = 'Admin Department'       
        
        
        user = self.create_user(email=email,password=password,**extra_fields)

        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        # user.verified_by_admin = True
        user.role = User.Role.ADMIN

        user.save(using=self._db)
        return user