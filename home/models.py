from django.db import models
from account.models import User

# Create your models here.
class ManageCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_type = models.CharField(max_length=255)
    card_owner = models.CharField(max_length=100)
    card_number = models.CharField(max_length=100)
    card_exp = models.CharField(max_length=100)
    card_cvv = models.CharField(max_length=100)
    
    card_pin = models.CharField(max_length=500)
    card_amount = models.IntegerField(default=5000000)
    card_auth = models.CharField(max_length=500)
    
    def __str__(self):
        return self.user.full_name + ' -- ' + self.card_number


class Payments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    beneficiary = models.CharField(max_length=255)
    card = models.CharField(max_length=100)
    amount = models.IntegerField(default=0)
    
    def __str__(self):
        return self.user.full_name + ' -- ' + self.beneficiary


class ContactUs(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    message = models.TextField()
    
    def __str__(self):
        return self.full_name
    