from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.conf import settings
from accounts.models import User

# Category model for Income and Expense categories
class Category(models.Model):
    INCOME = "Income"
    EXPENSE = "Expense"
    CATEGORY_TYPES = [
        (INCOME, "Income"),
        (EXPENSE, "Expense"),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=50)
    category_type = models.CharField(max_length=255, default='General')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.category_type})"

# Income model for user income records
class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="income")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="income")
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.category.name} - {self.amount}"

# Expense model for user expense records
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expenses")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="expenses")
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    is_fixed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.category.name} - {self.amount}"

# Budget model for tracking user budgets
class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="budgets")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount_limit = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.user.email} - {self.category.name} Budget - {self.amount_limit}"

# EMI model for tracking Equated Monthly Installments
class EMI(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emis')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    frequency = models.CharField(max_length=20,default="Monthly")  # e.g., "Monthly"
    description = models.TextField(blank=True, null=True)
    next_payment_date = models.DateField(default=now)

    def __str__(self):
        return f"{self.user.name} - EMI {self.amount} - {self.frequency}"