from django.db import models
from organization.models import CourseOrg, Teacher

# Create your models here.


class Course(models.Model):
    nid = models.BigAutoField(primary_key=True)
    name = models.CharField(verbose_name='课程名', max_length=50)
    course_org = models.ForeignKey(CourseOrg, verbose_name="课程机构", null=True, blank=True)
    describe = models.CharField(verbose_name='课程简介', max_length=255)
    detail = models.TextField(verbose_name='课程详情')
    teacher = models.ForeignKey(Teacher, verbose_name="讲师", null=True, blank=True)
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
    category = models.CharField(max_length=20, verbose_name="课程类别", default="后端开发")
    you_need_know = models.CharField(max_length=300, verbose_name="课程须知", default='')
    teacher_tell = models.CharField(max_length=300, verbose_name="老师告诉你", default='')
    is_banner = models.BooleanField(default=False, verbose_name="是否轮播")

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    # 获取课程章节数
    def get_zj_nums(self):
        return self.lesson_set.all().count()
    # 修改后台列名的显示，否则该列显示为 get_zj_nums
    get_zj_nums.short_description = "章节数"

    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    # 获取课程所有章节
    def get_course_lesson(self):
        return self.lesson_set.all()

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

    # 获取章节视频
    def get_lesson_video(self):
        return self.video_set.all()

    def __str__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(verbose_name='章节名', to='Lesson', to_field='nid')
    name = models.CharField(verbose_name='视频名', max_length=50)
    url = models.CharField(max_length=200, verbose_name="访问地址", default='')
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResouce(models.Model):
    course = models.ForeignKey(verbose_name='课程名', to='Course', to_field='nid')
    name = models.CharField(verbose_name='名称', max_length=50)
    download = models.FileField(upload_to='course/resource/%Y/%m', verbose_name='资源文件',max_length=100)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name