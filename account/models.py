from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from autoslug import AutoSlugField

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, full_name, ip, org, city, region, country, **extra_fields):
        if not full_name:
            raise ValueError('Enter fullname')
        if not email:
            raise ValueError('Invalid Email')
        if not password:
            raise ValueError('Password not correct')
        
        user = self.model(
            email = self.normalize_email(email),
            full_name = full_name,
            ip = ip,
            org = org,
            city = city,
            region = region,
            country = country,
            **extra_fields
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password, full_name, ip, org, city, region, country, **extra_fields):
        extra_fields.setdefault('is_admin', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_verified', False)
        return self._create_user(email, password, full_name, ip, org, city, region, country, **extra_fields)

    def create_superuser(self, email, password, full_name, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)
        return self._create_user(email, password, full_name, **extra_fields)



def default_profile_pic():
    return 'images/user.png'


class User(AbstractBaseUser, PermissionsMixin):
    # AbstractBaseUser has password, last_login and is_active by default
    email = models.EmailField(db_index=True, unique=True, max_length=255)
    full_name = models.CharField(max_length=255)
    ip = models.CharField(max_length=255, blank=True, null=True)
    org = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
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
    
    class Meta:
        ordering = ['-is_superuser', '-is_admin', '-is_verified']


class OneTimePassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True)
    
    def __str__(self):
        return self.user.email