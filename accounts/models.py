from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='user')
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} ({self.user_type})"
    
    @property
    def is_admin(self):
        return self.user_type == 'admin'
    
    @property
    def is_regular_user(self):
        return self.user_type == 'user'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    annual_income = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    monthly_savings = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    existing_loans = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    credit_score = models.IntegerField(default=300)
    employment_status = models.CharField(max_length=50, blank=True)
    employer_name = models.CharField(max_length=200, blank=True)
    years_employed = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    monthly_expenses = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    def __str__(self):
        return f"Profile: {self.user.username}"
