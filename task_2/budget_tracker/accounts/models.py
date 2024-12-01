from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "phone"]

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin

    def total_income(self):
        return sum([income.amount for income in self.income.all()])

    def total_expense(self):
        return sum([expense.amount for expense in self.expenses.all()])

    def total_savings(self):
        return self.total_income() - self.total_expense()
