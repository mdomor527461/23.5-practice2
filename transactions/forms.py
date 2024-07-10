from typing import Any
from django import forms
from .models import Transaction
from accounts.models import UserBankAccount
from transactions.constants import TRANSFER_MONEY,TRANSACTION_TYPE
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'amount',
            'transaction_type',
        ]
    
    def __init__(self, *args, **kwargs):
            self.request = kwargs.pop('request', None)
            self.account = kwargs.pop('account',None) # account value ke pop kore anlam
            super().__init__(*args, **kwargs)
            self.fields['transaction_type'].disabled = True # ei field disable thakbe
            self.fields['transaction_type'].widget = forms.HiddenInput() # user er theke hide kora thakbe

    def save(self, commit=True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance
        return super().save()


class DepositForm(TransactionForm):
    def clean_amount(self): # amount field ke filter korbo
        min_deposit_amount = 100
        amount = self.cleaned_data.get('amount') # user er fill up kora form theke amra amount field er value ke niye aslam, 50
        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f'You need to deposit at least {min_deposit_amount} $'
            )

        return amount



class WithdrawForm(TransactionForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean_amount(self):
        account = self.account
        min_withdraw_amount = 500
        max_withdraw_amount = 20000
        balance = account.balance
        amount = self.cleaned_data.get('amount')

        # Check if the bank is bankrupt
        if UserBankAccount.objects.filter(account_no = account.account_no,is_bankrupt = True).exists():
            raise forms.ValidationError(
                'Bank is bankrupt. Withdrawal is not allowed at this time.'
            )

        if amount < min_withdraw_amount:
            raise forms.ValidationError(
                f'You can withdraw at least {min_withdraw_amount} $'
            )

        if amount > max_withdraw_amount:
            raise forms.ValidationError(
                f'You can withdraw at most {max_withdraw_amount} $'
            )

        if amount > balance:
            raise forms.ValidationError(
                f'You have {balance} $ in your account. '
                'You cannot withdraw more than your account balance'
            )

        return amount

class LoanRequestForm(TransactionForm):
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')

        return amount


class TransferMoneyForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['recieving_account_no', 'amount']

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account')
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        sending_account = self.account
        recieving_account_no = cleaned_data.get('recieving_account_no')
        amount = cleaned_data.get('amount')

        
        
        if not recieving_account_no:
            raise forms.ValidationError('Recieving account number is required')

        if not amount:
            raise forms.ValidationError('Amount is required')

        if amount > sending_account.balance:
            print(amount,sending_account.balance)
            raise forms.ValidationError(
                f'You do not have sufficient balance to transfer {amount}$. Your current balance is {sending_account.balance}$.'
            )

        


        return cleaned_data
