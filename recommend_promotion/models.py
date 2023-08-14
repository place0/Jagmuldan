from django.db import models
from users.models import Restaurant
# Create your models here.
class Recommend(models.Model):
    month=models.IntegerField()
    crop=models.CharField(max_length=20)
    image=models.ImageField()
    detail=models.TextField()

class Promote(models.Model):
    restaurant=models.OneToOneField(Restaurant, on_delete=models.CASCADE, related_name='promote_restaurant')
