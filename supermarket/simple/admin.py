from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Category, Goods

# 配置后台管理文件
# 在admin 中注册绑定
"""
普通方法注册 装饰器方法注册
"""

admin.site.register(User, UserAdmin)
admin.site.register([Category, Goods])
