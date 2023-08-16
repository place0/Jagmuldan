from django.contrib import admin

# Register your models here.
from .models import *

class PhotoInline(admin.TabularInline):
    model = Photo

class RestaurantModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')  # 이 부분은 Restaurant 모델의 필드들을 적절하게 추가하셔야 합니다.
    search_fields = ('name',)
    inlines = [PhotoInline]

admin.site.register(Merchant)
admin.site.register(Restaurant, RestaurantModelAdmin)  # RestaurantModelAdmin을 사용하도록 등록
admin.site.register(User)
admin.site.register(LowIncome)
