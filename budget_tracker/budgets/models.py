from django.db import models
from accounts.models import User

class Category(models.Model):
    INCOME = "Income"
    EXPENSE = "Expense"
    CATEGORY_TYPES = [
        (INCOME, "Income"),
        (EXPENSE, "Expense"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=50)
    category_type = models.CharField(max_length=10, choices=CATEGORY_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.category_type})"

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="income")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="income")
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.category.name} - {self.amount}"

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

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="budgets")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount_limit = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.user.email} - {self.category.name} Budget - {self.amount_limit}"
