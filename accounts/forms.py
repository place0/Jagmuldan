from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import  UserCreationForm
# from shopping.models import Product
from users.models import User
from users.models import Merchant
from shopping.models import Product
#장고에서 제공하는 폼 커스텀


class FarmSignUpForm(UserCreationForm):
    farm_name = forms.CharField(max_length=50)
    description = forms.CharField(max_length=50)
    

    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2', 'farm_name', 'description']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Merchant.objects.create(user=user, farm_name=self.cleaned_data['farm_name'],description=self.cleaned_data['description'])
        return user


