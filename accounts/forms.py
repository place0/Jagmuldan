from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import  UserCreationForm
# from shopping.models import Product
from users.models import User
from users.models import Merchant, Restaurant, LowIncome
from shopping.models import Product


# 농장 회원가입 
class FarmSignUpForm(UserCreationForm):
    farm_name = forms.CharField(max_length=50)
    farm_adress = forms.CharField(max_length=50)
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2', 'farm_name', 'farm_adress']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Merchant.objects.create(user=user, farm_name=self.cleaned_data['farm_name'],farm_adress=self.cleaned_data['farm_adress'])
        return user

# 음식점 회원가입
class RestaurnatSignupForm(UserCreationForm):
    name = forms.CharField(max_length=50)
    address = forms.CharField(max_length=50)
    description=forms.CharField(max_length=50)

    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2', 'name', 'address','description']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Restaurant.objects.create(user=user, name=self.cleaned_data['name'],address=self.cleaned_data['address'], description=self.cleaned_data['description'])
        return user
    
# 일반 구매자 회원가입 
class UserSignupForm(UserCreationForm):
    class Meta:
        model=get_user_model()
        fields=['username','password1', 'password2']

# 저소득층 회원가입 
class LowIncomeSignupForm(UserCreationForm):
    image=forms.ImageField()
    class Meta:
        model=get_user_model()
        fields=['username','password1', 'password2', 'image']
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            LowIncome.objects.create(low_income=user, image=self.cleaned_data['image'])
        return user