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
    for product_id in selected_products:
        title = request.POST.get(f'product_title_{product_id}')
        price = int(request.POST.get(f'product_price_{product_id}').split('.')[0])
        price = int(float(price))
        quantity = int(request.POST.get(f'product_quantity_{product_id}').split('.')[0])
        quantity = int(float(quantity))
        half_purchased = request.POST.get(f'product_half_purchased_{product_id}') == 'True'

        # half_purchased인 경우 가격과 수량 조정
        if half_purchased:
            total_amount += price * quantity 
        else:
            total_amount += price * quantity
        
        item_names.append(title)
        
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
    if _result.get('msg'):
        return redirect('/payFail')
    else:
        # 주문 정보를 Order 모델에 저장
        selected_products = request.session.get('selected_products', [])
        for product_id in selected_products:
            product = Product.objects.get(pk=product_id)
            quantity = int(request.POST.get(f'product_quantity_{product_id}'))
            half_purchased = request.POST.get(f'product_half_purchased_{product_id}') == 'True'
            
            Order.objects.create(
                customer=request.user,
                product=product,
                quantity=quantity,
                half_purchased=half_purchased,
                time=datetime.now()
            )

            # 장바구니에서 해당 항목 제거
            basket_item = ShoppingBasket.objects.get(customer=request.user, product=product)
            basket_item.delete()

        return render(request, 'kakao/paySuccess.html')
def payFail(request):
    return render(request, 'kakao/payFail.html')
def payCancel(request):
    return render(request, 'kakao/payCancel.html')
