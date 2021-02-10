from django.db import models
import logging
import traceback

#gloabal parameters for site
class Ip_whitelist(models.Model):
    
    name = models.CharField(max_length = 250,default = "",verbose_name="App Name",unique=True)     #name of whitelisted app
    ip_address = models.GenericIPAddressField(default="0.0.0.0",verbose_name="IP Address")         #IP address 
    
    timestamp = models.DateTimeField(auto_now_add= True)
    updated= models.DateTimeField(auto_now= True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'White List IP'
        verbose_name_plural = 'White List IPs'