from django.shortcuts import render
from .models import *

def recommend_promotion(request):
    crops=Recommend.objects.all()
    restaurants=Promote.objects.all()
    return render(request, 'recommend_promotion/rp.html',{'crops':crops,'restaurants':restaurants} )



