from django.db import models

# Create your models here.
from django.db import models
from users.models import User
# Create your models here.
class JointShipping(models.Model):
    CATEGORY=[
        ('서울특별시','서울특별시'),
        ('경기도','경기도'),
        ('인천광역시','인천광역시'),
        ('강원특별자치도','강원특별자치도'),
        ('대전광역시','대전광역시'),
        ('세종특별자치도','세종특별자치도'),
        ('충청남도','충청남도'),
        ('충청북도','충청북도'),
        ('부산광역시','부산광역시'),
        ('울산광역시','울산광역시'),
        ('경상남도','경상남도'),
        ('경상북도','경상북도'),
        ('대구광역시','대구광역시'),
        ('광주광역시','광주광역시'),
        ('전라남도','전라남도'),
        ('전라북도','전라북도'),
        ('제주특별자치도','제주특별자치도'),
    ]
    detail=models.CharField(max_length=50, null=True)
    where = models.CharField( default='', max_length=10, choices=CATEGORY)
    url=models.URLField()
    title=models.CharField(max_length=50)
    context=models.TextField()
    writer=models.ForeignKey(User, related_name='writer',on_delete=models.CASCADE, null=True)

class Comment(models.Model):
    writer=models.BooleanField(default=False)
    context=models.CharField(max_length=50, null=True)
    community = models.ForeignKey(JointShipping, related_name='community',on_delete=models.CASCADE, null=True)

from users.models import Restaurant

class Review(models.Model):
    point=models.IntegerField()
    comment=models.CharField(max_length=500)
    restaurant=models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='restaurant_review')
    created_at = models.DateTimeField(auto_now_add=True)  
    image=models.ImageField(null=True)

    def __str__(self):
        return self.comment