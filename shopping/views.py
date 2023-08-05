from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.decorators import *
from django.http import HttpResponse
import json
from datetime import datetime, timedelta
from .models import Product
from django.http import JsonResponse

# 배송날짜 계산 함수
def get_next_business_day(current_date):
    # 현재 날짜에서 2일을 더한 날짜를 계산
    target_date = current_date + timedelta(days=2)
    
    # 일요일을 제외한 다음 영업일을 찾음
    while target_date.weekday() in [6]: 
        target_date += timedelta(days=1)
    
    return target_date

# 메인페이지
def index(request):
    products=Product.objects.all()
    best=products[0]
    for p in products:
        if p.like_product.count() > best.like_product.count():
            best=p
    return render(request, 'shopping/index.html',{'products':products,'best':best})

    
# 상품 등록
def upload(request):
    if request.method=='GET':
        return render(request, 'shopping/upload.html')
    else:
        
        title=request.POST['title']
        price=int(request.POST['price'])
        origin=request.POST['origin']
        feature=request.POST['feature']
        type=request.POST['type']
        product=Product()
        product.title=title
        product.type=type
        
        product.price=price
        product.production_features=feature
        product.origin=origin
        product.discount_rate=0
        product.seller=request.user.merchant
        product.save()
        for img in request.FILES.getlist('imgs'):
            photo = Photo()
            photo.product = product
            photo.image = img
            photo.save()
        
        return redirect('index')
    
# 상품 상세페이지
def detail(request, id):
    product = get_object_or_404(Product, id=id)
    discount_rate = product.discount_rate or 0
    discount_price = product.price * (1 - discount_rate / 100)
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        user_id = request.user.id
        quantity = int(quantity)

        action = request.POST.get('action')
        print(action)
        if action == 'purchase':
            return redirect('index')

        elif action == 'goto_basket':
        
            user = User.objects.get(pk=user_id)
            order, created = ShoppingBasket.objects.get_or_create(customer=user, product=product, defaults={'quantity': quantity})

            if not created:
                order.quantity += quantity
                order.save()

    return render(request, 'shopping/detail.html', {'product': product,'discount_price': discount_price})

# 좋아요
def add_remove_whishlist(request):
    if request.method == "POST" and request.is_ajax():
        product_id = request.POST.get("product_id")
        product = get_object_or_404(Product, id=product_id)
        user = request.user
        liked = False

        if product in user.like_product.all():
            # 이미 좋아요한 상품이라면 제거
            user.like_product.remove(product)
        else:
            # 아직 좋아요하지 않은 상품이라면 추가
            user.like_product.add(product)
            liked = True

        return JsonResponse({"liked": liked})
    return JsonResponse({}, status=400)

# 마이페이지
def mypage(request):
    products=request.user.like_product.all()
    return render(request,'shopping/mypage.html',{'products':products})

# 내 상품 조회
def my_product(request):
    products=Product.objects.filter(seller=request.user.merchant)
    return render(request,'shopping/my_product.html',{'products':products})

# 찜한 목록 조회
def wishlist(request):
    products=request.user.like_product.all()
    return render(request,'shopping/wishlist.html',{'products':products})

# 정보 수정
def update_user(request):
    if request.method=="GET":
        return render(request,'shopping/update_user.html')
    else:
        description=request.POST['description']
        farm_name=request.POST['farm_name']
        new_image=request.FILES.get('image')
        user=Merchant.objects.get(user=request.user)
        if new_image:
            if user.image != 'Koala.png':
                user.image.delete()
                user.image=new_image
        user.description=description
        user.farm_name=farm_name
        user.save()
        return redirect('mypage')
    
# 등록 상품 삭제
def delete_product(reuqest,id):
    product=get_object_or_404(Product, id=id)
    product.delete()
    return redirect('my_product')

# 상품 등록 수정
def update_upload(request, id):
    product=get_object_or_404(Product, id=id)
    if request.method=="GET":
        return render(request,'shopping/update_upload.html',{'product':product})
    else:
        title=request.POST['title']
        price=int(request.POST['price'])
        origin=request.POST['origin']
        feature=request.POST['feature']
        type=request.POST['type']

        product.title=title
        product.price=price
        product.origin=origin
        product.production_features=feature
        product.type=type
        product.save()
        if request.FILES.getlist('imgs'):
            for img in product.product_image.all():
                img.delete()
            for img in request.FILES.getlist('imgs'):
                # Photo 객체를 하나 생성한다.
                photo = Photo()
                # 외래키로 현재 생성한 Post의 기본키를 참조한다.
                photo.product = product
                # imgs로부터 가져온 이미지 파일 하나를 저장한다.
                photo.image = img
                # 데이터베이스에 저장
            photo.save()
        return redirect('my_product')

# 장바구니
def basket(request):
    # GET 요청일 경우에는 모든 상품 목록을 출력
    products = ShoppingBasket.objects.filter(customer=request.user)
    total_price = sum(p.product.price * p.quantity for p in products)
    current_date = datetime.now().date()
    arrive_day = get_next_business_day(current_date)
    return render(request, 'shopping/basket.html', {'products': products, 'total_p': total_price, 'arrive_day':arrive_day})

# 장바구니 삭제
def basket_delete(request, id):
    product = get_object_or_404(Product, id=id)
    try:
        order = ShoppingBasket.objects.get(product=product)
        order.delete()
    except ShoppingBasket.DoesNotExist:
        pass
    return redirect('basket')

def final(request):
    if request.method == "POST":
        selected_products = request.POST.getlist('selected_products')
        total_price = 0
        products = ShoppingBasket.objects.filter(customer=request.user, product__id__in=selected_products)
        request.session['selected_products'] = selected_products  # 선택한 제품의 ID 리스트 저장
        for p in products:
            total_price += p.product.price * p.quantity
        valid_coupon = []
        for c in request.user.coupons.all():
            if c.is_valid == True:
                valid_coupon.append(c)
        return render(request, 'shopping/purchase.html', {'products': products, 'total_p': total_price, 'valid_coupon': valid_coupon})
    else:  # GET 요청인 경우
        selected_product_ids = request.session.get('selected_products', [])  # 선택한 제품의 ID 리스트 가져오기
        products = ShoppingBasket.objects.filter(customer=request.user, product__id__in=selected_product_ids)  # 해당 제품들 조회
        total_price = sum(p.product.price * p.quantity for p in products)  # 가격 계산
        valid_coupon = []
        for c in request.user.coupons.all():
            if c.is_valid == True:
                valid_coupon.append(c)
        return render(request, 'shopping/purchase.html', {'products': products, 'total_p': total_price, 'valid_coupon': valid_coupon})

@login_required
# @require_POST # 해당 뷰는 POST method 만 받는다.
def product_like(request):
    pk = request.POST.get('pk', None) # ajax 통신을 통해서 template에서 POST방식으로 전달
    product = get_object_or_404(Product, pk=pk)
    product_like, product_like_created = Product.like_set.get_or_create(user=request.user)

    if not product_like_created:
        product_like.delete()
        message = "좋아요 취소"
    else:
        message = "좋아요"

    context = {'like_count': product.like_count,
               'message': message,
               'nickname': request.user.profile.nickname }
    
    return HttpResponse(json.dumps(context), content_type="application/json")