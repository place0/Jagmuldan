from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout

# Create your views here.
def signup(request):
    return render(request, 'accounts/signup.html')
        
from django.shortcuts import render, redirect
from .forms import FarmSignUpForm

def merchant_signup(request):
    if request.method == 'POST':
        form = FarmSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # 회원가입이 성공한 경우 리다이렉트 등을 처리
            return redirect('index')
    else:
        form = FarmSignUpForm()
    return render(request, 'accounts/merchant_signup.html', {'form': form})


        
def login_view(request):
    #get,post분리
    if request.method=='GET':
        #로그인 html 파일 응답 
        return render(request, 'accounts/login.html',{'form':AuthenticationForm()})
    else: 
        #데이터 유효성 검사
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid(): 
            #비즈니스 로직 처리 - 로그인 성공 - 로그인처리 
            login(request, form.user_cache)  #로그인 처리를 하는 함수
            #응답
            return redirect('index') #인덱스 페이지로 돌려보냄 
        else:
            #비즈니스 로직 처리 - 로그인 실패
            #응답
            return render(request, 'accounts/login.html',{'form':form})
        
def logout_view(request):
    #유효성 검사
    if request.user.is_authenticated:  #프로퍼티라고 설정되어 있어서 괄호 없어도 됨 
        #비즈니스 로직 처리-로그아웃
        logout(request)
    #응답 
    return redirect('index')