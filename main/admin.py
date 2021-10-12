from django.contrib import admin
from main.models import *

# Register your models here.
admin.site.register(Ip_whitelist)
admin.site.register(Parameters)

class PaymentsAdmin(admin.ModelAdmin):
            
      ordering = ['-timestamp']
      list_display = ['email', 'amount', 'memo', 'timestamp']

admin.site.register(Payments, PaymentsAdmin)
