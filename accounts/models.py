from django.db import models
from django.contrib.auth.models import User
from accounts.constant import GENDER_TYPE,ACCOUNT_TYPE



# Create your models here.
class UserBankAccount(models.Model):
    user = models.OneToOneField(User,related_name='account',on_delete= models.CASCADE)
    
    account_type = models.CharField(max_length=100,choices=ACCOUNT_TYPE)
    account_no = models.IntegerField(unique=True)
    gender = models.CharField(max_length=100,choices=GENDER_TYPE)
    birth_date = models.DateField(null = True,blank=True)
    first_deposit_date = models.DateField(auto_now_add=True)
    balance = models.DecimalField(default=0,max_digits=12,decimal_places=2)
    is_bankrupt = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.account_no)
    
class UserAdress(models.Model):
    user = models.OneToOneField(User,related_name='address',on_delete=models.CASCADE)
    
    street_address = models.CharField(max_length=100)
    postal_code = models.IntegerField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user.username