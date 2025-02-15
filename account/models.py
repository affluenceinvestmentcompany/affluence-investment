from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def _create_user(self, full_name, email, phone, password, **extra_fields):
        if not email:
            raise ValueError('Enter valid email')
        email = self.normalize_email(email)
        user = self.model(full_name=full_name, email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, full_name, email, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_verified', False)
        return self._create_user(full_name, email, phone, password, **extra_fields)

    def create_superuser(self, full_name, email, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)
        return self._create_user(full_name, email, phone, password, **extra_fields)

def default_profile_pic():
    return 'images/user.png'

class User(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(db_index=True, unique=True, max_length=255)
    phone = models.CharField(max_length=255, default='Not Provided')
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to='profile_pics', default=default_profile_pic, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'phone']
    
    class Meta:
        ordering = ['-is_superuser', '-is_admin', '-is_staff', '-is_verified', '-date_joined']

    def __str__(self):
        return self.email
    
    def delete(self):
        self.profile_image.delete()
        super().delete()


class OneTimePassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True)
    
    def __str__(self):
        return self.user.email


class ResetPassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uid = models.CharField(max_length=256, unique=True)
    token = models.CharField(max_length=256, unique=True)
    
    def __str__(self):
        return str(self.user.id)