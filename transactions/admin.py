from django.contrib import admin
from . views import transaction_email
# from transactions.models import Transaction
from .models import Transaction
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['account', 'amount', 'balance_after_transaction', 'transaction_type', 'loan_approve']
    
    def save_model(self, request, obj, form, change):
        obj.account.balance += obj.amount
        obj.balance_after_transaction = obj.account.balance
        obj.account.save()
        transaction_email(obj.account.user,"Admin Approval Message",obj.amount,'transactions/admin_approve_email.html')
        super().save_model(request, obj, form, change)
