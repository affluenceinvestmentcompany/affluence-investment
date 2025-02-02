from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from autoslug import AutoSlugField

class CustomUserManager(BaseUserManager):
    def _create_user(self, full_name, email, phone, password, **extra_fields):
        if not full_name:
            raise ValueError('Enter fullname')
        if not email:
            raise ValueError('Invalid Email')
        if not phone:
            raise ValueError('Invalid Phone')
        if not password:
            raise ValueError('Password not correct')
        
        user = self.model(
            email = self.normalize_email(email),
            full_name = full_name,
            phone = phone,
            **extra_fields
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, full_name, phone, email, password, **extra_fields):
        extra_fields.setdefault('is_admin', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_verified', False)
        return self._create_user(full_name, phone, email, password, **extra_fields)

    def create_superuser(self, full_name, phone, email, password, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)
        return self._create_user(full_name, phone, email, password, **extra_fields)



def default_profile_pic():
    return 'images/user.png'


class User(AbstractBaseUser, PermissionsMixin):
    # AbstractBaseUser has password, last_login and is_active by default
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField(db_index=True, unique=True, max_length=255)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to='profile_pics', default=default_profile_pic, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    def delete(self):
        self.profile_image.delete()
        super().delete()

class OneTimePassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True)
    
    def __str__(self):
        return self.user.email
    
    