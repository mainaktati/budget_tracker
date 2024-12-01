from django.core.management.base import BaseCommand
from budgets.models import EMI, Category
from django.utils.timezone import now

class Command(BaseCommand):
    help = "Automatically process EMI payments due today."

    def handle(self, *args, **kwargs):
        # Ensure "EMI" category exists
        if not Category.objects.filter(name="EMI").exists():
            Category.objects.create(name="EMI", type="Expense")

        # Process EMI payments that are due today
        due_emis = EMI.objects.filter(next_payment_date__lte=now().date(), remaining_installments__gt=0)
        for emi in due_emis:
            emi.pay_installment()
            self.stdout.write(f"Processed EMI payment for {emi.user.email}, Amount: {emi.amount}")
