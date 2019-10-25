from django.urls import path
from . import views

# 应用级路由 用来连接各个网页和视图
urlpatterns = [
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('detail/<int:goods_id>/', views.detail, name='detail'),
    path('register/', views.register, name='register'),
    path('info/', views.user_center_info, name='user_center_info'),
    path('cart/', views.cart, name='cart'),
    path('cart_del/', views.cart_del, name='cart_del'),
    path('place_order/', views.place_order, name='place_order'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('order/', views.user_center_order, name='user_center_order'),
    path('site/', views.user_center_site, name='user_center_site'),
    path('place_order/', views.place_order, name='place_order'),
    path('create_order/', views.create_order, name='create_order'),
    path('logout/', views.logout, name='logout'),
    path('del_order/', views.del_order, name='del_order'),
    path('receive_address/', views.receive_address, name='receive_address'),
    path('create_receive_address/', views.create_receive_address, name='create_receive_address'),
    path('list/<int:category_id>/', views.goods_list, name='list_first_page'),
    path('list/<int:category_id>/<int:p>/', views.goods_list, name='list'),
    path('update_cart_number/<int:goods_id>/<int:number>/', views.update_cart_number, name='update_cart_number'),
]
