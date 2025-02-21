from django.db import models
from account.models import User
from django.utils.timezone import now
from decimal import Decimal


SIXTY_SECOND_PERCENTAGE_RATES = {
    "BASIC": Decimal("0.008") / Decimal("1440"),   # 0.8% daily
    "STANDARD": Decimal("0.01") / Decimal("1440"),  # 1.0% daily
    "PREMIUM": Decimal("0.012") / Decimal("1440"),  # 1.2% daily
    "ULTIMATE": Decimal("0.015") / Decimal("1440"), # 1.5% daily
}

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
    plan = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=13, decimal_places=2)
    roi = models.DecimalField(max_digits=13, decimal_places=2, default=Decimal("0.00"))
    pending = models.BooleanField(default=True)
    active = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(null=True, blank=True)

    def update_roi(self):
        if not self.active:
            # print(f"Skipping {self.plan} (Inactive)")
            return
        last_updated = self.last_updated or self.date
        current_time = now()
        elapsed_seconds = (current_time - last_updated).total_seconds()
        intervals = Decimal(elapsed_seconds) // Decimal(60)
        if intervals < 1:
            # print(f"Skipping {self.plan}: Not enough time passed ({elapsed_seconds} seconds)")
            return
        normalized_plan = self.plan.strip().upper()
        rate = SIXTY_SECOND_PERCENTAGE_RATES.get(normalized_plan, Decimal("0"))
        if rate == Decimal("0"):
            # print(f"Skipping {self.plan}: No rate found")
            return
        new_roi = self.amount * rate * intervals
        self.roi += new_roi
        self.last_updated = current_time
        self.save()
        # print('\n||||||||||||||||||||||||||||||\n')
        # print(f"Updated {self.plan}: +{new_roi}, New ROI: {self.roi}")
        # print('\n||||||||||||||||||||||||||||||\n')

    def __str__(self):
        return f"{self.user.full_name} -- {self.plan} -- {self.amount}"


class Withdrawal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=13, decimal_places=2)
    method = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    processing = models.BooleanField(default=True)
    completed = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.user.full_name} -- {self.plan} -- {self.amount}"


class Transactions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    method = models.ForeignKey(Payments, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=13, decimal_places=2)
    bonus = models.DecimalField(max_digits=13, decimal_places=2)
    pending = models.BooleanField(default=True)
    confirmed = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.user.full_name} -- {self.amount}"

