from django.urls import path
from .views import *

app_name='accounts'
urlpatterns = [
        # 기본 회원가입 화면
    path('', signup, name='signup'),
    # 판매자 회원가입 화면
    path('merchant/', merchant_signup, name='merchant_signup'),
    path('restaurnat/', restaurant_signup, name='restaurant_signup'),
    path('user/', user_signup, name='user_signup'),
    path('low_income/', low_income_signup, name='low_income_signup'),
    
    path('login/',login_view, name='login'),
    path('logout/',logout_view, name='logout'),
    
]