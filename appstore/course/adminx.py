__author__ = 'Jeff'


from .models import Course, Lesson, Video, CourseResouce
from extra_apps import xadmin


class CourseAdmin():
    list_display = ['name', 'describe', 'detail', 'students', 'recive_num', 'click_num', 'image',
                    'create_time', 'degree', 'learn_times', 'teacher']
    search_fields = ['name', 'describe', 'detail', 'students', 'recive_num', 'click_num', 'image',
                     'degree', 'learn_times', 'teacher']
    list_filter = ['name', 'describe', 'detail', 'students', 'recive_num', 'click_num', 'image',
                   'create_time', 'degree', 'learn_times', 'teacher']


class LessonAdmin():
    list_display = ['course', 'name', 'create_time']
    search_fields = ['name', 'course']
    list_filter = ['course__name', 'name', 'create_time']


class VideoAdmin():
    list_display = ['lesson', 'name', 'create_time']
    search_fields = ['name', 'lesson']
    list_filter = ['name', 'lesson__name', 'create_time']


class CourseResouceAdmin():
    list_display = ['course', 'name', 'download', 'create_time']
    search_fields = ['name', 'course', 'download']
    list_filter = ['name', 'course__name', 'download', 'create_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResouce, CourseResouceAdmin)