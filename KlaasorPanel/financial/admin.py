from django.contrib import admin
from .models import OfflinePaymentDetail, Payment, Invoice

# Register your models here.


admin.site.register(OfflinePaymentDetail)
admin.site.register(Payment)
admin.site.register(Invoice)
