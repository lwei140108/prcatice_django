from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from .forms import RegisterForm
from .models import Category, Goods, Cart, OrderInfo, ReceiveAddress, User, OrderGoods
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import json
from django.db.models import Sum, F


# def base(request):
#     """父模板"""
#     categories = Category.objects.all()
#     context = {
#         'categories': categories
#     }
#     return render(request, 'base.html', context)


def index(request):
    """首页"""
    categories = Category.objects.all()
    goods = Goods.objects.all()
    context = {
        'categories': categories,
        'goods': goods
    }
    return render(request, 'index.html', context)


def login(request):
    """登陆页面"""
    if request.method == 'POST':

        # AuthenticationForm 表单验证 自带
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            # 重定向页面 get 是字典中的方法 第二个参数是默认值 next存储的路由地址
            response = redirect(request.POST.get('next', 'index'))
            return response

    else:
        form = AuthenticationForm()
    context = {
        'form': form,
        'next': request.GET.get('next', 'index')
        }
    return render(request, 'login.html', context)


def logout(request):
    """退出"""
    auth_logout(request)
    return redirect('index')


def register(request):
    """注册页面"""
    if request.method == 'POST':

        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            response = redirect(request.POST.get('next', 'index'))
            return response
        else:
            redirect('login')
    else:
        form = RegisterForm()
    context = {
        'form': form
    }
    return render(request, 'register.html', context)


def user_center_info(request):
    customer = ReceiveAddress.objects.get(is_default=True)
    context = {
        'customer': customer
    }
    return render(request, 'user_center_info.html', context)


def cart(request):
    """展示购物车列表页面"""
    data_list = []
    if request.user.is_authenticated:
        data_list = Cart.objects.filter(user=request.user)
    else:
        pass
    context = {
        'data_list': data_list
    }
    return render(request, 'cart.html', context)


def cart_del(request):
    goods_del_id = request.GET.get('goods_id')
    Cart.objects.filter(id=goods_del_id, user=request.user).delete()
    return redirect('cart')


def add_to_cart(request,):
    """把商品添加到购物车"""
    try:
        goods_id = request.GET.get("goods_id")
        goods = Goods.objects.get(pk=goods_id)
    except ObjectDoesNotExist:
        return render(request, 'add_to_cart.html')
    number = int(request.GET.get('number'))
    categories = Category.objects.all()
    context = {
        'goods': goods,
        'number': number,
        'categories': categories,

    }
    if request.user.is_authenticated:
        try:
            item = Cart.objects.get(user=request.user, goods_id=goods_id)
            item.number += number
            item.save()

        except ObjectDoesNotExist:
            Cart.objects.create(user=request.user, goods_id=goods_id, number=number)
        response = render(request, 'add_to_cart.html', context)
    else:
        response = render(request, 'index.html', context)
    return response


@login_required
def user_center_order(request):
    """用户订单中心"""
    all_order = OrderInfo.objects.filter(user=request.user)
    order_goods = OrderGoods.objects.filter(orderinfo__in=all_order)
    context = {
        'all_order': all_order,
        'order_goods': order_goods,
    }
    return render(request, 'user_center_order.html', context)


def user_center_site(request):
    """用户中心收货地址页面"""
    return render(request, 'user_center_site.html')


def goods_list(request, category_id, p=None):
    """商品列表"""
    try:
        current_category = Category.objects.get(pk=category_id)
        goods = current_category.goods_set.all()
    except ObjectDoesNotExist:
        return HttpResponseNotFound('商品不存在')
    # 分页功能 一页展示2件商品
    paginator = Paginator(goods, 2)
    page = paginator.get_page(p)
    categories = Category.objects.all()
    context = {
        'current_category': current_category,
        'page': page,
        'categories': categories,
    }
    return render(request, 'list.html', context)


def detail(request, goods_id):
    """商品详情"""
    try:
        goods = Goods.objects.get(pk=goods_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound('商品不存在')
    categories = Category.objects.all()
    context = {
        'goods': goods,
        'categories': categories,
    }
    return render(request, 'detail.html', context)


def update_cart_number(request, goods_id, number):
    """异步更新购物车商品的数量"""
    rows = Cart.objects.filter(user=request.user, goods_id=goods_id).update(number=number)
    return JsonResponse({'success': rows > 0})


@login_required
def place_order(request):
    """提交订单处理"""
    ids = request.GET.get('ids')
    # 显示默认地址
    # recver = ReceiveAddress.objects.get(is_default='True')

    if ids is not None:
        carts = Cart.objects.filter(user=request.user, goods_id__in=json.loads(ids))
        # aggregate 合计 carts.aggregate(count=Sum('number')) 获取的值是一个字典
        count = carts.aggregate(count=Sum('number'))['count']
        total = 0
        for item in carts:
            total += item.goods.price * item.number
        context = {
            "carts": carts,
            "count": count,
            "total": total,

        }
        response = render(request, 'place_order.html', context)
    else:
        response = HttpResponseNotFound()
    return response


def create_order(request):
    address_id = request.POST.get('address_id')

    cart_ids = request.POST.get('cart_ids')
    print(cart_ids)
    amount = request.POST.get('amount')
    orderinfo = OrderInfo.objects.create(user=request.user, receive_address_id=address_id, amount=amount)

    if orderinfo is not None:
        print("订单创建成功")
        for cart1 in Cart.objects.filter(id__in=json.loads(cart_ids)):
            orderinfo.ordergoods_set.create(
                goods=cart1.goods,
                number=cart1.number,
                price=cart1.goods.price,
            )
            print("订单货物创建成功")
            cart1.delete()
        return JsonResponse({
            'success': True
        })
    orderinfo.delete()
    return JsonResponse({
        'success': False
    })


def receive_address(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, "receive_address.html", context)


@login_required
def create_receive_address(request):
    region = request.POST.get("region")
    name = request.POST.get('name')
    details = request.POST.get('detail')
    tel = request.POST.get('tel')
    is_default = request.POST.get('default')

    address = ReceiveAddress.objects.create(region=region, name=name, detail=details, tel=tel, user=request.user,
                                            is_default=is_default)

    if address is not None:
        # return JsonResponse({
        #     'success': True
        # })
        return redirect('user_center_info')
    else:
        # return JsonResponse({
        #     "success": False
        # })
        return redirect('user_center_site')


def del_order(request):
    order_id = request.GET.get('orders_id')
    print(order_id)
    order_info = OrderInfo.objects.all()
    order_info.filter(id=order_id).delete()
    return redirect('user_center_order')


