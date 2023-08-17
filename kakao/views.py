from django.shortcuts import render, redirect
import requests
from django.http import HttpResponse
from shopping.models import Product, ShoppingBasket, Order
from datetime import datetime

def kakaoPay(request):
    return render(request, 'shopping/basket.html')
def kakaoPayLogic(request):
    selected_products = request.POST.getlist('selected_products')
    total_amount = 0  # 총 결제 금액
    item_names = []   # 상품 이름 리스트
    selected_products_data = []
    for product_id in selected_products:
        title = request.POST.get(f'product_title_{product_id}')
        price = int(request.POST.get(f'product_price_{product_id}').split('.')[0])
        price = int(float(price))
        quantity = int(request.POST.get(f'product_quantity_{product_id}').split('.')[0])
        quantity = int(float(quantity))
        half_purchased = request.POST.get(f'product_half_purchased_{product_id}') == 'True'

        # half_purchased인 경우 가격과 수량 조정
        if half_purchased:
            total_amount += price * quantity * 2
        else:
            total_amount += price * quantity
        
        item_names.append(title)
        
        selected_products_data.append({
                'id': product_id,
                'title': title,
                'price': price,
                'quantity': quantity,
                'half_purchased': half_purchased
        })
    
    print(request.POST.get('product_delivery'))
    print(request.POST.get('product_coupon'))
    

    print(total_amount)
    total_amount+=int(request.POST.get('product_delivery'))-int(request.POST.get('product_coupon'))
    print(total_amount)

        
    _admin_key = '4c5a240e7c426e334c4ef4808ff9dc02'
    _url = f'https://kapi.kakao.com/v1/payment/ready'
    _headers = {
        'Authorization': f'KakaoAK {_admin_key}',
    }
    _data = {
        'cid': 'TC0ONETIME',
        'partner_order_id':'partner_order_id',
        'partner_user_id':'partner_user_id',
        'item_name': ', '.join(item_names),
        'quantity': len(selected_products),
        'total_amount': str(total_amount),
        'vat_amount':'200',
        'tax_free_amount':'0',
        # 내 애플리케이션 -> 앱설정 / 플랫폼 - WEB 사이트 도메인에 등록된 정보만 가능합니다
        # * 등록 : http://IP:8000 
        'approval_url':'http://127.0.0.1:8000/paySuccess', 
        'fail_url':'http://127.0.0.1:8000/payFail',
        'cancel_url':'http://127.0.0.1:8000/payCancel'
    }
    _res = requests.post(_url, data=_data, headers=_headers)
    _result = _res.json()
    request.session['tid'] = _result['tid']
    request.session['selected_products_data'] = selected_products_data
    return redirect(_result['next_redirect_pc_url'])

def paySuccess(request):
    
    _url = 'https://kapi.kakao.com/v1/payment/approve'
    _admin_key = '4c5a240e7c426e334c4ef4808ff9dc02' # 입력필요
    _headers = {
        'Authorization': f'KakaoAK {_admin_key}'
    }
    _data = {
        'cid':'TC0ONETIME',
        'tid': request.session['tid'],
        'partner_order_id':'partner_order_id',
        'partner_user_id':'partner_user_id',
        'pg_token': request.GET['pg_token']
    }
    _res = requests.post(_url, data=_data, headers=_headers)
    _result = _res.json()
    selected_products_data = request.session.get('selected_products_data', [])
    for product_data in selected_products_data:
        product = Product.objects.get(pk=product_data['id'])
        quantity = product_data['quantity']
        half_purchased = product_data['half_purchased']

        Order.objects.create(
            customer=request.user,
            product=product,
            quantity=quantity,
            half_purchased=half_purchased,
            time=datetime.now()
        )
    
        # 장바구니에서 해당 항목 제거
        basket_item = ShoppingBasket.objects.filter(customer=request.user, product=product).first()
        if basket_item:  # 조건 확인
            basket_item.delete()


    return render(request, 'shopping/basket.html')
def payFail(request):
    return render(request, 'shopping/basket.html')
def payCancel(request):
    return render(request, 'shopping/basket.html')
