__author__ = 'Jeff'


from .models import Course, Lesson, Video, CourseResouce
from extra_apps import xadmin


class LessonInline(object):
    model = Lesson
    extra = 0


class CourseResourceInline(object):
    model = CourseResouce
    extra = 0


class CourseAdmin():
    list_display = ['name', 'describe', 'detail', 'students', 'recive_num', 'click_num', 'image',
                    'create_time', 'degree', 'learn_times', 'teacher', 'get_zj_nums']
    search_fields = ['name', 'describe', 'detail', 'students', 'recive_num', 'click_num', 'image',
                     'degree', 'learn_times', 'teacher']
    list_filter = ['name', 'describe', 'detail', 'students', 'recive_num', 'click_num', 'image',
                   'create_time', 'degree', 'learn_times', 'teacher']
    ordering = ['-click_num']
    readonly_fields = ['click_num', 'recive_num']

    inlines = [LessonInline, CourseResourceInline]#一页修改多个model

    # 在保存课程的时候，统计课程机构的课程数
    def save_models(self):
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()


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