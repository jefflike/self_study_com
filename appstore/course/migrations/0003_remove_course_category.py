# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-01 14:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_course_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='category',
        ),
    ]