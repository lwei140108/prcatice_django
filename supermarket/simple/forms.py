# -*-coding:utf-8-*-
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User, Cart

# form.py是Django用来生成form表单代码和验证表单数据是否合法的一个文件, 可以在该文件中创建Form类, 实现自定义表单的功能
# 改写Django 字带的表单验证功能 添加新的验证调节


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields
    email = forms.EmailField(label='邮箱')


class CarCreationForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ('user', 'goods', 'number')