# -*-coding:utf-8-*-
from django import template
from django.db.models import Sum
from simple.models import Category, Cart
import json

# 定义模板标签 可以在HTML页面直接使用
register = template.Library()


@register.simple_tag
def get_categories():
    """获得所有分类"""
    return Category.objects.all()


@register.simple_tag(takes_context=True)
def get_cart_count(context):
    """获得购物车商品的总数量"""
    request = context.get('request')
    count = 0
    if request.user.is_authenticated:
        result = Cart.objects.filter(user=request.user).aggregate(count=Sum('number'))
        count = result.get('count')
    else:
        cart_goods = request.COOKIES.get('cart_goods')
        if cart_goods is not None:
            cart_goods = json.load(cart_goods.replace('\'', '\"'))
            for v in cart_goods.values():
                count += int(v)
    return count


@register.simple_tag
def multiply(num1, num2):
    return num1 * num2
