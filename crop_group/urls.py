from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from kakao import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('shopping.urls')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    # path('restaurnats/',include('review.urls', namespace='review')),
    path('community/',include('community.urls', namespace='community')),
    path('recommend_promote/',include('recommend_promotion.urls', namespace='recommend_promotion')),
    path('kakaoPay/', views.kakaoPay),
    path('kakaoPayLogic/', views.kakaoPayLogic),
    path('paySuccess/', views.paySuccess),
    path('payFail/', views.payFail),
    path('payCancel/', views.payCancel),
    path('paySuccess/' ,views.paySuccess, name='paySuccess'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)