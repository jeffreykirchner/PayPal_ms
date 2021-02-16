'''
site wide parameters
'''
#import logging
#import traceback

from django.db import models

#gloabal parameters for site
class Parameters(models.Model):
    '''
    site wide parameters
    '''
    contact_email =  models.CharField(max_length = 1000,default = "JohnSmith@abc.edu")      #contact email 

    max_daily_earnings = models.DecimalField(decimal_places=2, max_digits=5,default = 100)    #max money that can be paid to a subject per year  
    site_URL = models.CharField(max_length = 200,default = "https://www.google.com/")         #site URL used for display in emails
    
    paypal_token = models.CharField(max_length = 200,default = "asdf123")                            #token used for paypal requests
    #paypal_note = models.CharField(max_length = 200,default = "Thanks for your participation!")     #note sent along with paypal payment

    timestamp = models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return f"Site Parameters {self.contact_email} {self.max_daily_earnings}"

    class Meta:
        verbose_name = 'Site Parameters'
        verbose_name_plural = 'Site Parameters'