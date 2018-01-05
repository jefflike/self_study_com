from django.db import models
from django.contrib.auth.models import  AbstractUser

# Create your models here.


class UserInfo(AbstractUser):
    """
    用户表
    """
    nickname = models.CharField(verbose_name='昵称', max_length=32)
    address = models.CharField(verbose_name='地址', max_length=100)
    cellphone_number = models.CharField(verbose_name='手机号', max_length=11)
    birthday = models.DateField(verbose_name='生日', null=True, blank=True,)
    avatar = models.ImageField(verbose_name='头像', upload_to='static/imgs/%Y/%m',default='static/imgs/default.png')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    sex_choices = [
        ("male", "男"),
        ("female", "女"),
    ]
    sex = models.CharField(choices=sex_choices, default='male', verbose_name='性别', max_length=6)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    # 获取用户未读消息数量
    def unread_nums(self):
        from operation.models import UserMessage
        return UserMessage.objects.filter(user=self.id, has_read=False).count()

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    email_choices = (
        ('register', '注册'),
        ('forget', '找回密码'),
        ("update_email", "修改邮箱")
    )
    code = models.CharField(max_length=20, verbose_name='验证码')
    email = models.EmailField(max_length=50, verbose_name='邮箱')
    send_type = models.CharField(choices=email_choices, max_length=13, verbose_name='验证码类型')
    send_time = models.DateTimeField(auto_now_add=True, verbose_name='发送时间')

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)


class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name='标题')
    image = models.ImageField(upload_to='banner/%Y/%m', verbose_name='轮播图', max_length=100)
    url = models.URLField(max_length=200, verbose_name='访问地址')
    index = models.IntegerField(default=100, verbose_name='顺序')
    add_time = models.DateField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name


# 全局 404 处理函数
def page_not_found(request):
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


# 全局 404 处理函数
def page_error(request):
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response