from django.db import models

from django.contrib.auth.models import User, AbstractUser, BaseUserManager

from django.conf import settings

from datetime import datetime

# User = settings.AUTH_USER_MODEL



class MyUserManager(BaseUserManager):
    def create_user(self, student_id, phone_number, email, password=None):
            user = self.model(student_id=student_id,
                        phone_number=phone_number,
                        email=email
                        )
            user.set_password(password)
            user.save(using=self._db)
            return user

    def create_superuser(self, student_id, email, password, *args, **kwargs):
        user = self.create_user(student_id, None, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
        

class User(AbstractUser):
    username = models.CharField(max_length=150, null=True, blank=True)
    student_id = models.CharField(max_length=8, unique=True)
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    last_name = models.CharField(max_length=20)
    first_name = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)

    objects = MyUserManager()
    USERNAME_FIELD = 'student_id'
    
    def __str__(self):
        return self.last_name + " " + (self.first_name or "")







# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     phone_number = models.CharField(max_length=11)
#     student_id = models.CharField(max_length=8)