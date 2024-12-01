# budgets/forms.py

from django import forms
from .models import EMI,Income

class EMIForm(forms.ModelForm):
    class Meta:
        model = EMI
        fields = ['amount', 'start_date', 'end_date', 'frequency', 'description', 'next_payment_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'next_payment_date': forms.DateInput(attrs={'type': 'date'}),
        }

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['category', 'amount', 'description', 'date']