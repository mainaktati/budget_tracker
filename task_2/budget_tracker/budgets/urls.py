from django.urls import path
from . import views
from .views import dashboard, add_income, add_expense,add_category

# app_name = 'budgets'

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("add-income/", add_income, name="add_income"),
    path("add-expense/", add_expense, name="add_expense"),
    path("add-category/", add_category, name="add_category"),
    path('clear-dashboard-data/', views.clear_dashboard_data, name='clear_dashboard_data'),
    path("add-emi/", views.add_emi, name="add_emi"),
    path("emi-list/", views.emi_list, name="emi_list"),
    
    path('income/<int:income_id>/update/', views.update_or_delete_income, name='update_or_delete_income'),
    path('expense/<int:expense_id>/update/', views.update_or_delete_expense, name='update_or_delete_expense'),
]