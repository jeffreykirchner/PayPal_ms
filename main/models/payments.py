# import logging
# import traceback

from django.db import models

from . import Ip_whitelist

from django.contrib.auth.models import User

#gloabal parameters for site
class Payments(models.Model):
    '''
    payments model
    '''

    email =  models.EmailField(max_length = 250)                     #email of payee
    amount = models.DecimalField(decimal_places=2, max_digits=5)     #payment amount
    memo = models.CharField(max_length = 250,default = "")           #momo recorded about payment
    note = models.CharField(max_length = 250,default = "")           #note shown in body of the email
    
    app = models.ForeignKey(User,on_delete=models.CASCADE,related_name="app_name")

    payout_batch_id_local = models.CharField(max_length = 250,default = "")    #batch payment id locally assinged
    payout_batch_id_paypal = models.CharField(max_length = 250,default = "")   #batch payment id asigned by paypal

    timestamp = models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return f'{self.email} {self.amount} {self.memo}'

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['-timestamp']
        