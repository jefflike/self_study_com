from django.db import models

# Create your models here.


class CityDict(models.Model):
    nid = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='城市名', max_length=50)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    describe = models.CharField(verbose_name='城市简介', max_length=255)

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    nid = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='组织名', max_length=50)
    describe = models.CharField(verbose_name='机构简介', max_length=255)
    choices = [
        ('pxjg', "培训机构"),
        ('gr', "个人"),
        ('gx', "高校"),
    ]
    category = models.CharField(max_length=20, verbose_name='机构类别', choices=choices, default='pxjg')
    students = models.IntegerField(default=0, verbose_name='学习人数')
    receive_num = models.IntegerField(default=0, verbose_name='收藏人数')
    click_num = models.IntegerField(default=0, verbose_name='点击人数')
    courses_nums = models.IntegerField(default=0, verbose_name="课程数")
    image = models.ImageField(upload_to='org/%Y/%m', verbose_name='封面图', max_length=100)
    address = models.CharField(verbose_name='机构地址', max_length=100)
    city = models.ForeignKey(verbose_name='所在城市名', to='CityDict', to_field='nid')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '课程机构'
        verbose_name_plural = verbose_name

    def get_teacher_nums(self):
        # 获取课程机构的教师数量
        return self.teacher_set.all().count()

    def __str__(self):
        return self.name


class Teacher(models.Model):
    nid = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='教师名', max_length=50)
    describe = models.CharField(verbose_name='教师简介', max_length=255)
    work_year = models.IntegerField(default=0, verbose_name='工作年限')
    address = models.ForeignKey(verbose_name='所在地址', to='CityDict', to_field='nid')
    concern_num = models.IntegerField(default=0, verbose_name='关注人数')
    org = models.ForeignKey(verbose_name='所属机构', to='CourseOrg', to_field='nid')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
    age = models.IntegerField(default=18, verbose_name="年龄")
    image = models.ImageField(default="", upload_to="teacher/%Y/%m", verbose_name="头像", max_length=100)

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name