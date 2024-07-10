from django.contrib import admin
from . models import UserBankAccount,UserAdress
# Register your models here.
admin.site.register(UserBankAccount)
admin.site.register(UserAdress)