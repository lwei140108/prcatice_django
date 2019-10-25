from django.db import models
from django.contrib.auth.models import AbstractUser

# 数据库模型 每一个类代表一张数据表 变量代表表中的字段名


class User(AbstractUser):
    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
    nickname = models.CharField('昵称', max_length=20, null=True)
    avatar = models.ImageField('头像')
    # choices 将在页面中展示后一个原素，在数据库中存储前面的数字 在页面中获取的方法是 obj.get_字段名_display:
    sex = models.SmallIntegerField('性别', choices=((0, '女'), (1, '男'), (2, '保密')), default=2)
    mobile = models.CharField('手机', max_length=11, null=True)
    birthday = models.DateField('生日', null=True)
    pay_pwd = models.CharField('支付密码', max_length=6, null=True)


class Category(models.Model):
    class Meta:
        # 起名字
        verbose_name = '商品分类'
        # 名字的复数形式
        verbose_name_plural = verbose_name
    name = models.CharField('名称', max_length=20, unique=True)
    icon_class = models.CharField('图标样式', max_length=30)
    # upload_to 指定的是上传图片存放的路径，会自动追加为media的子目录
    banner = models.ImageField('广告图', upload_to='category/')

    def __str__(self):
        return self.name


class Goods(models.Model):
    class Meta:
        verbose_name = '商品信息'
        verbose_name_plural = verbose_name
        ordering = ('-price',)
    name = models.CharField('名称', max_length=60)
    picture = models.ImageField('主图', upload_to='goods/')
    price = models.DecimalField('价格', max_digits=6, decimal_places=2)
    desc = models.CharField('描述', max_length=100)
    unit = models.CharField('单位', max_length=20)
    stock = models.IntegerField('库存')
    detail = models.TextField('详情')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='分类')

    # 魔术方法 返回自身的名字 用处 在后台管理界面显示
    def __str__(self):
        return self.name


class Cart(models.Model):
    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = verbose_name
    # 设置外键 在字表中设置 一对多的关系 字段名为主表名字的小写 on_delete=models.CASCADE 固定写法
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='商品')
    number = models.SmallIntegerField('数量')


class ReceiveAddress(models.Model):
    class Meta:
        verbose_name = '收货地址'
        verbose_name_plural = verbose_name
    region = models.CharField('所在区域', max_length=100)
    name = models.CharField('收货人', max_length=20)
    detail = models.CharField('详细地址', max_length=100)
    email = models.EmailField('邮箱', null=True)
    alias = models.CharField('地址别名', max_length=20, null=True)
    is_default = models.BooleanField('默认地址', default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    tel = models.CharField('手机', max_length=11)


class OrderInfo(models.Model):
    class Meta:
        verbose_name = '订单信息'
        verbose_name_plural = verbose_name
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    # 用于页面上的选择框标签，需要先提供一个二维的二元元组，第一个元素表示存在数据库内真实的值，
    # 第二个表示页面上显示的具体内容。在浏览器页面上将显示第二个元素的值
    # 要获取一个choices的第二元素的值，可以使用get_FOO_display()方法，其中的FOO用字段名代替
    status = models.SmallIntegerField('订单状态', choices=((0, '未完成'), (1, '已完成')), default=0)
    pay_status = models.SmallIntegerField('支付状态', choices=((0, '未支付'), (1, '已支付')), default=0)
    created_date = models.DateTimeField('订单日期', auto_now_add=True)
    goods = models.ManyToManyField(Goods, through='OrderGoods', through_fields=('orderinfo', 'goods'))
    amount = models.DecimalField('总金额', max_digits=8, decimal_places=2)
    receive_address = models.ForeignKey(ReceiveAddress, on_delete=models.CASCADE, verbose_name='收货地址', null=True)


class OrderGoods(models.Model):
    class Meta:
        verbose_name = '订单商品'
        verbose_name_plural = verbose_name

    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='商品')
    orderinfo = models.ForeignKey(OrderInfo, on_delete=models.CASCADE, verbose_name='订单')
    number = models.SmallIntegerField('数量')
    price = models.DecimalField('价格', max_digits=6, decimal_places=2)
