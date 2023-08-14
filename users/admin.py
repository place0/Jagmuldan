from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Merchant)

admin.site.register(Restaurant)
admin.site.register(User)
admin.site.register(LowIncome)

