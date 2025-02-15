from django.db import models
from account.models import User

# Create your models here.
class Payments(models.Model):
    method = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    
    # qrcode = models.ImageField(upload_to='profile_pics')
    
    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return self.method 


class Packages(models.Model):
    plan = models.CharField(max_length=255)
    profit = models.CharField(max_length=100)
    bonus = models.CharField(max_length=100)
    min_amount = models.CharField(max_length=100)
    min_days = models.CharField(max_length=100)
    goto_url = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return self.plan 


class Investments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=255)
    amount = models.CharField(max_length=100)
    roi = models.CharField(max_length=100)
    pending = models.BooleanField(default=True)
    active = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return self.user.full_name + ' -- ' + self.plan


class Withdrawal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.CharField(max_length=255)
    withdraw = models.CharField(max_length=100)
    processing = models.BooleanField(default=True)
    completed = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return self.user.full_name + ' -- ' + self.withdraw


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    method = models.ForeignKey(Payments, on_delete=models.CASCADE)
    amount = models.CharField(max_length=100)
    bonus = models.CharField(max_length=100)
    pending = models.BooleanField(default=True)
    confirmed = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return self.user.full_name + ' -- ' + self.amount

