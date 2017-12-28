from django.db import models
from users.models import UserInfo
from course.models import Course

# Create your models here.


class UserAsk(models.Model):
    nid = models.BigAutoField(primary_key=True)
    name = models.CharField(verbose_name='姓名', max_length=50)
    mobile = models.CharField(verbose_name='手机号', max_length=11)
    course_name = models.CharField(verbose_name='要报课程', max_length=50)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '用户咨询'
        verbose_name_plural = verbose_name


class Comment(models.Model):
    """
    评论表
    """
    nid = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(UserInfo,verbose_name='评论者')
    course = models.ForeignKey(Course,verbose_name='评论课程', to_field='nid')
    content = models.CharField(verbose_name='评论内容', max_length=255)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '课程评论'
        verbose_name_plural = verbose_name


class UserFavorite(models.Model):
    user = models.ForeignKey(UserInfo, verbose_name='收藏者')
    fav_id = models.IntegerField(default=0, verbose_name='数据id')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    type_choices = [
        (1, "课程"),
        (2, "课程机构"),
        (3, "讲师"),
    ]
    fav_type = models.IntegerField(choices=type_choices, default=None, verbose_name='收藏类型')

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    nid = models.BigAutoField(primary_key=True)
    user = models.IntegerField(default=0, verbose_name='接收用户')
    message = models.CharField(verbose_name='消息内容', max_length=500)
    has_read = models.BooleanField(default=False, verbose_name='是否已读')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '用户消息'
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    nid = models.IntegerField(primary_key=True)
    user = models.ForeignKey(UserInfo,verbose_name='用户')
    course = models.ForeignKey(Course,verbose_name='课程', to_field='nid')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name