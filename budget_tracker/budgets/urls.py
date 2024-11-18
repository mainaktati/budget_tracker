from django.urls import path
from . import views
from .views import dashboard, add_income, add_expense,add_category

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("add-income/", add_income, name="add_income"),
    path("add-expense/", add_expense, name="add_expense"),
    path("add-category/", add_category, name="add_category"),
    path('clear-dashboard-data/', views.clear_dashboard_data, name='clear_dashboard_data'),
]
