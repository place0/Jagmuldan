from django.urls import path
from .views import *

app_name='community'
urlpatterns = [
    path('',main, name='main'),
    path('<int:id>/comments/',create_review, name='comments'),
    path('create_shopping_together/',create_shopping_together,name='create_shopping_together'),
    path('detail_together/<int:id>/',detail_together, name='detail_together'),
]