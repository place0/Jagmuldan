from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def _create_user(self, username, email, password, **extra_fields):
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff',False)  #이메일 부분 제거 
        extra_fields.setdefault('is_superuser',False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff',True)  
        extra_fields.setdefault('is_superuser',True)
        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    address = models.CharField(max_length=100, null=True)
    like_product = models.ManyToManyField('shopping.Product',  related_name='like_product')
    purchased = models.ManyToManyField('shopping.Product', related_name='purchased')
    objects = CustomUserManager()

    def __str__(self):
        return self.username
    
class Merchant(models.Model):
    description=models.CharField(max_length=50) # 한줄소개
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='merchant')
    image = models.ImageField(upload_to='merchant/', default='merchant/Koala.png')
    farm_name = models.CharField(max_length=50)


    def __str__(self):
        return self.farm_name
