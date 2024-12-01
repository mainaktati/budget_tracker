# budgets/admin.py

from django.contrib import admin
from .models import EMI

class EMIAdmin(admin.ModelAdmin):
    # Correctly reference 'user' and 'remaining_installments_display'
    list_display = ('user', 'amount', 'start_date', 'end_date', 'frequency')
    list_filter = ('user',)  # Correctly reference 'user' for filtering
    
    # Method to display the remaining installments in the admin
    # def remaining_installments_display(self, obj):
    #     return obj.remaining_installments
    # remaining_installments_display.short_description = 'Remaining Installments'

admin.site.register(EMI, EMIAdmin)
