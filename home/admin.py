from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register((Payments, Packages, Investments, Transactions, Withdrawal))
