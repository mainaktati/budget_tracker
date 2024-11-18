from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Income, Expense, Budget, Category
from django.utils.timezone import now
from django.urls import reverse
from django.http import HttpResponseBadRequest


@login_required
def dashboard(request):
    incomes = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)
    budgets = Budget.objects.filter(user=request.user)

    total_income = sum(income.amount for income in incomes)
    total_expense = sum(expense.amount for expense in expenses)
    savings = total_income - total_expense

    return render(request, "budgets/dashboard.html", {
        "incomes": incomes,
        "expenses": expenses,
        "budgets": budgets,
        "total_income": total_income,
        "total_expense": total_expense,
        "savings": savings,
    })

@login_required
def add_income(request):
    categories = Category.objects.filter(user=request.user, category_type="Income")
    if not categories.exists():
        return redirect(reverse('add_category') + f"?type=Income")

    if request.method == "POST":
        category = Category.objects.get(id=request.POST["category"])
        amount = request.POST["amount"]
        description = request.POST["description"]
        date = request.POST["date"]
        Income.objects.create(user=request.user, category=category, amount=amount, description=description, date=date)
        return redirect("dashboard")

    return render(request, "budgets/add_income.html", {"categories": categories})

@login_required
def add_expense(request):
    # Get categories for the current user that are of type 'Expense'
    categories = Category.objects.filter(user=request.user, category_type="Expense")
    
    # Redirect user to add categories if no categories exist
    if not categories.exists():
        return redirect(reverse('add_category') + "?type=Expense")  # Adjust 'add_category' to match your actual URL name

    if request.method == "POST":
        category_id = request.POST.get("category")
        amount = request.POST.get("amount")
        description = request.POST.get("description")
        date = request.POST.get("date")

        # Validate category selection
        try:
            category = Category.objects.get(id=category_id, user=request.user)
            Expense.objects.create(
                user=request.user,
                category=category,
                amount=amount,
                description=description,
                date=date
            )
            return redirect("dashboard")  # Replace 'dashboard' with your desired redirect path
        except Category.DoesNotExist:
            return render(request, "budgets/add_expense.html", {
                "categories": categories,
                "error": "Invalid category selected."
            })

    return render(request, "budgets/add_expense.html", {"categories": categories})

@login_required
def add_category(request):
    if request.method == "POST":
        name = request.POST.get("name")
        category_type = request.POST.get("type", "Expense").capitalize()  # Default to Expense
        Category.objects.create(user=request.user, name=name, category_type=category_type)

        # Redirect back to the referring page if available
        next_url = request.POST.get("next")
        if next_url:
            return redirect(next_url)

        return redirect("add_expense" if category_type == "Expense" else "add_income")
    
    category_type = request.GET.get("type", "Expense")
    return render(request, "budgets/add_category.html", {"category_type": category_type})

@login_required
def clear_dashboard_data(request):
    if request.method == "POST":
        # Delete all income records
        Income.objects.filter(user=request.user).delete()

        # Delete all expense records
        Expense.objects.filter(user=request.user).delete()

        # Delete or reset any summary data (or delete it if applicable)
        # Summary.objects.filter(user=request.user).delete()  # Adjust depending on your model

        # After clearing the data, redirect back to the dashboard
        return redirect('dashboard')  # Replace 'dashboard' with the actual URL name of your dashboard page
    else:
        # If not a POST request, redirect back to the dashboard
        return redirect('dashboard')