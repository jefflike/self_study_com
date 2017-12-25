# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-25 09:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('nid', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='课程名')),
                ('describe', models.CharField(max_length=255, verbose_name='课程简介')),
                ('detail', models.TextField()),
                ('students', models.IntegerField(default=0, verbose_name='学习人数')),
                ('recive_num', models.IntegerField(default=0, verbose_name='收藏人数')),
                ('click_num', models.IntegerField(default=0, verbose_name='点击人数')),
                ('image', models.ImageField(upload_to='course/%Y/%m', verbose_name='封面图')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('degree', models.CharField(choices=[('simple', '初级'), ('middle', '中级'), ('difficult', '难')], default=None, max_length=10)),
                ('learn_times', models.IntegerField(default=0, verbose_name='课程时长（分钟）')),
            ],
            options={
                'verbose_name': '课程',
                'verbose_name_plural': '课程',
            },
        ),
        migrations.CreateModel(
            name='CourseResouce',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='章节名')),
                ('download', models.FileField(upload_to='course/resource/%Y/%m', verbose_name='资源文件')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Course', verbose_name='课程名')),
            ],
            options={
                'verbose_name': '课程资源',
                'verbose_name_plural': '课程资源',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('nid', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='章节名')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Course', verbose_name='课程名')),
            ],
            options={
                'verbose_name': '章节',
                'verbose_name_plural': '章节',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='章节名')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Lesson', verbose_name='章节名')),
            ],
            options={
                'verbose_name': '视频',
                'verbose_name_plural': '视频',
            },
        ),
    ]
