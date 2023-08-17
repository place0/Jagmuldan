from django.urls import path
from .views import *
urlpatterns = [
    path('',index, name='index'),
    # path('get_products_by_type/', get_products_by_type, name='get_products_by_type'),

    path('post/create/', upload, name='upload'),
    path('detail/<int:id>/',detail,name='detail'),

    path('mypage/',mypage, name='mypage'),
    path('my_product/',my_product, name='my_product'),
    path('update_user_merchant/',update_user_merchant, name='update_user_merchant'),
    path('update_user_restaurant/',update_user_restaurant, name='update_user_restaurant'),
    
    path('update_upload/<int:id>/',update_upload, name='update_upload'),
    path('delete_product/<int:id>/',delete_product, name='delete_product'),  
    
    path('wishlist/',wishlist, name='wishlist'),
    path('basket/',basket, name='basket'),
    path('basket_delete/<int:id>/', basket_delete, name='basket-delete'),


    # path('like/<int:id>/',product_like, name='product_like'),
    path('add_remove_whishlist/<int:id>/', add_remove_whishlist, name='add_remove_whishlist'),
    
    path('half_purchased/', half_purchased_products, name='half_purchased_products'),
    # path('restaurant/review/')
    path('half_ing/', half_purchased_products, name='half_ing'),
]
