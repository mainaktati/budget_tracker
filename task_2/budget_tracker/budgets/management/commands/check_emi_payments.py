from django.core.management.base import BaseCommand
from budgets.models import EMI
from django.utils import timezone

class Command(BaseCommand):
    help = 'Check and add expense for any due EMI payments'

    def handle(self, *args, **kwargs):
        emís = EMI.objects.all()  # Get all EMIs
        today = timezone.now().date()  # Get today's date

        for emi in emís:
            if emi.next_payment_date <= today and emi.remaining_installments > 0:
                # If next payment date has passed and installments remain
                emi.add_expense_on_repayment()  # Add the expense for this EMI
                self.stdout.write(self.style.SUCCESS(f"EMI for {emi.start_date} processed and expense added."))
            else:
                self.stdout.write(self.style.WARNING(f"EMI for {emi.start_date} not due yet."))
