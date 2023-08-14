from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('shopping.urls')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    # path('restaurnats/',include('review.urls', namespace='review')),
    path('community/',include('community.urls', namespace='community')),
    path('recommend_promote/',include('recommend_promotion.urls', namespace='recommend_promotion'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)