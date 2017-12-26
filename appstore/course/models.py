from django.db import models

# Create your models here.


class Course(models.Model):
    nid = models.BigAutoField(primary_key=True)
    name = models.CharField(verbose_name='课程名', max_length=50)
    describe = models.CharField(verbose_name='课程简介', max_length=255)
    detail = models.TextField(verbose_name='课程详情')
    students = models.IntegerField(default=0, verbose_name='学习人数')
    recive_num = models.IntegerField(default=0, verbose_name='收藏人数')
    click_num = models.IntegerField(default=0, verbose_name='点击人数')
    image = models.ImageField(upload_to='course/%Y/%m', verbose_name='封面图', max_length=100)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    type_choices = [
        ('simple', "初级"),
        ('middle', "中级"),
        ('difficult', "难"),
    ]
    degree = models.CharField(choices=type_choices, default=None, max_length=10, verbose_name='课程难度')
    learn_times = models.IntegerField(default=0, verbose_name='课程时长（分钟）')

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Lesson(models.Model):
    nid = models.BigAutoField(primary_key=True)
    course = models.ForeignKey(verbose_name='课程名', to='Course', to_field='nid')
    name = models.CharField(verbose_name='章节名', max_length=50)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(verbose_name='章节名', to='Lesson', to_field='nid')
    name = models.CharField(verbose_name='章节名', max_length=50)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name


class CourseResouce(models.Model):
    course = models.ForeignKey(verbose_name='课程名', to='Course', to_field='nid')
    name = models.CharField(verbose_name='章节名', max_length=50)
    download = models.FileField(upload_to='course/resource/%Y/%m', verbose_name='资源文件',max_length=100)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name