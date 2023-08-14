from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.http import HttpResponse

# Create your views here.
def main(request):
    places=[
            '서울특별시','경기도','인천광역시'
            '강원특별자치도',
            '대전광역시','세종특별자치도','충청남도', '충청북도',
            '부산광역시'
            '울산광역시',
            '경상남도',
            '경상북도',
            '대구광역시',
            '광주광역시',
            '전라남도',
            '전라북도',
            '제주특별자치도',
        ]
    restaurants = Restaurant.objects.all()
    asks=JointShipping.objects.all()
    page=False
    if request.session.get('page'):
        page=True
        del request.session['page']

    if request.method=="POST":
        search=request.POST['search']
        action=request.POST['action']
        if action=="restaurant_search":
            restaurants=Restaurant.objects.filter(name__contains=search)
        if action=="local_search":
            where=request.POST['where']
            asks=JointShipping.objects.filter(detail__contains=search, where=where)
            page=True
    context={
        'restaurants':restaurants,
        'asks':asks,
        'places':places,
        'page':page
    }
    print(page)
    return render(request, 'community/main.html', context)

def create_review(request, id):
    restaurant=get_object_or_404(Restaurant, id=id)
    if request.method=="POST":
        comment=request.POST['comment']
        point=request.POST['point']
        
        Review.objects.create(
            restaurant=restaurant, 
            comment=comment,
            point=point,
            )
        return redirect('community:comments', id=id)
        
    comments=Review.objects.filter(restaurant=restaurant)
    context={
        'r':restaurant,
        'comments':comments
    }
    return render(request, 'community/comments.html',context)
    
def create_shopping_together(request):
    places=[
            '서울특별시','경기도','인천광역시'
            '강원특별자치도',
            '대전광역시','세종특별자치도','충청남도', '충청북도',
            '부산광역시'
            '울산광역시',
            '경상남도',
            '경상북도',
            '대구광역시',
            '광주광역시',
            '전라남도',
            '전라북도',
            '제주특별자치도',
        ]
    if request.method=="POST":
        js=JointShipping()
        js.where=request.POST['where']
        js.url=request.POST['url']
        js.title=request.POST['title']
        js.context=request.POST['context']
        js.detail=request.POST['detail']
        js.writer=request.user
        js.save()
        request.session['page']=True
        return redirect('community:main')
    return render(request, 'community/create_shopping_together.html', {'places':places})

def detail_together(request, id):
    ask=get_object_or_404(JointShipping, id=id)
    if request.method=="POST":
        context=request.POST['context']
        print(ask.writer)
        print(request.user)
        if ask.writer == request.user:
            writer=True
        else:
            writer=False
        print(writer)
        Comment.objects.create(
            context=context,
            community=ask,
            writer=writer
        )
        return redirect('community:detail_together', id=id)
    context={'ask':ask}
    return render(request, 'community/detail_together.html', context)


