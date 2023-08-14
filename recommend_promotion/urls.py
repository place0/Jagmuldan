from django.urls import path
from .views import *

app_name='recommend_promotion'
urlpatterns = [
    path('',recommend_promotion, name='rp')
    
]