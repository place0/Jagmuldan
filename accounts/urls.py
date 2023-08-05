from django.urls import path
from .views import *

app_name='accounts'
urlpatterns = [
        # 기본 회원가입 화면
    path('', signup, name='signup'),
    # 판매자 회원가입 화면
    path('merchant/', merchant_signup, name='merchant_signup'),
    path('login/',login_view, name='login'),
    path('logout/',logout_view, name='logout'),
    
]