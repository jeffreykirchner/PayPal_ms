from django.db import models
import logging
import traceback
from django.contrib.auth.models import User

#gloabal parameters for site
class Parameters(models.Model):

    contactEmail =  models.CharField(max_length = 1000,default = "JohnSmith@abc.edu")      #contact email 

    maxDailyEarnings = models.DecimalField(decimal_places=2, max_digits=5,default = 100)    #max money that can be paid to a subject per year  
    siteURL = models.CharField(max_length = 200,default = "https://www.google.com/")        #site URL used for display in emails
    
    timestamp = models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return "Site Parameters"

    class Meta:
        verbose_name = 'Parameters'
        verbose_name_plural = 'Parameters'