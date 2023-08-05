from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import User
from users.models import Merchant
class Product(models.Model):
    seller = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='products')
    title=models.CharField(max_length=100)
    price = models.IntegerField()
    discount_rate = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    origin = models.CharField(max_length=100)
    production_features = models.TextField()
    type = models.CharField(choices=(('채소','채소'),('과일','과일')), default="과일", max_length=2)
    
# 여러개의 이미지
class Photo(models.Model):
    product = models.ForeignKey(Product, related_name='product_image',on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='product_photos/', blank=True, null=True)

# 장바구니
class ShoppingBasket(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, related_name='basket_product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

