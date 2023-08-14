from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout
from users.models import Photo
# Create your views here.

#회원가입 유형 선택
def signup(request):
    return render(request, 'accounts/signup.html')
        
from django.shortcuts import render, redirect
from .forms import FarmSignUpForm, RestaurnatSignupForm

# 음식점 회원가입
def restaurant_signup(request):
    if request.method == 'POST':
        form = RestaurnatSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=True)  # 유저 정보 저장
            for img in request.FILES.getlist('imgs'):
                photo = Photo()
                photo.restaurant = user.restaurant  # 유저와 이미지 연결
                photo.image = img
                photo.save()

            return redirect('index')
    else:
        form = RestaurnatSignupForm()
    return render(request, 'accounts/restaurant_signup.html', {'form': form})

# 판매자 회원가입
def merchant_signup(request):
    if request.method == 'POST':
        form = FarmSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = FarmSignUpForm()
    return render(request, 'accounts/merchant_signup.html', {'form': form})

# 일반 고객 회원가입
def user_signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = UserSignupForm()
    return render(request, 'accounts/user.html', {'form': form})

# 저소득층 회원가입
def low_income_signup(request):
    if request.method == 'POST':
        form = LowIncomeSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()  # User 저장
            return redirect('index')
    else:
        form = LowIncomeSignupForm()
    return render(request, 'accounts/low_income_signup.html', {'form': form})


# 로그인 
def login_view(request):
    if request.method=='GET':
        return render(request, 'accounts/login.html',{'form':AuthenticationForm()})
    else: 
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid(): 
            login(request, form.user_cache)  
            return redirect('index') 
        else:
            return render(request, 'accounts/login.html',{'form':form})

# 로그아웃     
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('index')