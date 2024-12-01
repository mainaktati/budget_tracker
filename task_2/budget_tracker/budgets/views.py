from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Income, Expense, Budget, Category, EMI
from .forms import EMIForm, IncomeForm
from django.utils.timezone import now
from django.urls import reverse
from django.http import HttpResponseBadRequest

from django.db.models import Sum

@login_required
def dashboard(request):
    # Fetch income and expense records for the logged-in user
    incomes = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)
    emis = EMI.objects.filter(user=request.user)

    # Calculate total income, expense, and savings
    total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = (
        expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    ) + (
        emis.aggregate(Sum('amount'))['amount__sum'] or 0
    )
    savings = total_income - total_expense

    # Combine expenses and EMIs into a single list for the dashboard
    combined_expenses = list(expenses) + [
        Expense(
            date=emi.next_payment_date, 
            category=Category(name="EMI: " + emi.description), 
            amount=emi.amount
        ) 
        for emi in emis
    ]

    context = {
        'incomes': incomes,
        'expenses': combined_expenses,  # Use the combined list
        'total_income': total_income,
        'total_expense': total_expense,
        'savings': savings,
    }
    return render(request, 'budgets/dashboard.html', context)

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
    categories = Category.objects.filter(user=request.user, category_type="Expense")
    
    if not categories.exists():
        return redirect(reverse('add_category') + "?type=Expense")

    if request.method == "POST":
        category_id = request.POST.get("category")
        amount = request.POST.get("amount")
        description = request.POST.get("description")
        date = request.POST.get("date")

        try:
            category = Category.objects.get(id=category_id, user=request.user)
            Expense.objects.create(
                user=request.user,
                category=category,
                amount=amount,
                description=description,
                date=date
            )
            return redirect("dashboard")
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

        next_url = request.POST.get("next")
        if next_url:
            return redirect(next_url)

        return redirect("add_expense" if category_type == "Expense" else "add_income")
    
    category_type = request.GET.get("type", "Expense")
    return render(request, "budgets/add_category.html", {"category_type": category_type})

@login_required
def clear_dashboard_data(request):
    if request.method == "POST":
        Income.objects.filter(user=request.user).delete()
        Expense.objects.filter(user=request.user).delete()
        EMI.objects.filter(user=request.user).delete()
        return redirect('dashboard')
    else:
        return redirect('dashboard')
    

@login_required
def add_emi(request):
    if request.method == 'POST':
        form = EMIForm(request.POST)
        if form.is_valid():
            emi = form.save(commit=False)
            emi.user = request.user
            emi.save()
            return redirect('emi_list')
    else:
        form = EMIForm()
    return render(request, 'budgets/add_emi.html', {'form': form})

@login_required
def emi_list(request):
    emis = EMI.objects.filter(user=request.user)
    return render(request, 'budgets/emi_list.html', {'emis': emis})

@login_required
def update_or_delete_income(request, income_id):
    # Fetch the income object for the given ID and ensure it belongs to the current user
    income = get_object_or_404(Income, id=income_id, user=request.user)

    # Get categories for the current user that are of type 'Income'
    categories = Category.objects.filter(user=request.user, category_type="Income")

    if request.method == "POST":
        if "update" in request.POST:
            # Handle Update Action
            category_id = request.POST.get("category")
            amount = request.POST.get("amount")
            description = request.POST.get("description")
            date = request.POST.get("date")

            if not category_id or not amount or not date:
                # Validate required fields
                return render(request, "budgets/update_or_delete_income.html", {
                    "income": income,
                    "categories": categories,
                    "error": "All fields are required."
                })

            try:
                category = Category.objects.get(id=category_id, user=request.user)
                # Update the income object
                income.category = category
                income.amount = float(amount)  # Ensure amount is a valid number
                income.description = description
                income.date = date
                income.save()
                return redirect("dashboard")  # Redirect to dashboard after update
            except Category.DoesNotExist:
                return render(request, "budgets/update_or_delete_income.html", {
                    "income": income,
                    "categories": categories,
                    "error": "Invalid category selected."
                })
            except ValueError:
                return render(request, "budgets/update_or_delete_income.html", {
                    "income": income,
                    "categories": categories,
                    "error": "Amount must be a valid number."
                })

        elif "delete" in request.POST:
            # Handle Delete Action
            income.delete()
            return redirect("dashboard")  # Redirect after deletion

    # Render the template for GET requests
    return render(request, "budgets/update_or_delete_income.html", {
        "income": income,
        "categories": categories
    })


@login_required
def update_or_delete_expense(request, expense_id):
    # Fetch the expense object for the given ID and ensure it belongs to the current user
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)

    # Get categories for the current user that are of type 'Expense'
    categories = Category.objects.filter(user=request.user, category_type="Expense")

    if request.method == "POST":
        if "update" in request.POST:
            # Handle Update Action
            category_id = request.POST.get("category")
            amount = request.POST.get("amount")
            description = request.POST.get("description")
            date = request.POST.get("date")

            if not category_id or not amount or not date:
                # Validate required fields
                return render(request, "budgets/update_or_delete_expense.html", {
                    "expense": expense,
                    "categories": categories,
                    "error": "All fields are required."
                })

            try:
                category = Category.objects.get(id=category_id, user=request.user)
                # Update the expense object
                expense.category = category
                expense.amount = float(amount)  # Ensure amount is a valid number
                expense.description = description
                expense.date = date
                expense.save()
                return redirect("dashboard")  # Redirect to dashboard after update
            except Category.DoesNotExist:
                return render(request, "budgets/update_or_delete_expense.html", {
                    "expense": expense,
                    "categories": categories,
                    "error": "Invalid category selected."
                })
            except ValueError:
                return render(request, "budgets/update_or_delete_expense.html", {
                    "expense": expense,
                    "categories": categories,
                    "error": "Amount must be a valid number."
                })

        elif "delete" in request.POST:
            # Handle Delete Action
            expense.delete()
            return redirect("dashboard")  # Redirect after deletion

    # Render the template for GET requests
    return render(request, "budgets/update_or_delete_expense.html", {
        "expense": expense,
        "categories": categories
    })
