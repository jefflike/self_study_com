__author__ = 'Jeff'


from extra_apps import xadmin
from .models import CityDict, CourseOrg, Teacher


class CityDictAdmin():
    list_display = ['name', 'describe', 'create_time']
    search_fields = ['name', 'describe']
    list_filter = ['name', 'describe', 'create_time']


class CourseOrgAdmin():
    list_display = ['name', 'describe', 'students', 'receive_num', 'click_num', 'image',
                    'create_time', 'address', 'city']
    search_fields = ['name', 'describe', 'students', 'receive_num', 'click_num', 'image',
                     'create_time', 'address', 'city']
    list_filter = ['name', 'describe', 'students', 'receive_num', 'click_num', 'image',
                   'create_time', 'address', 'city__name']


class TeacherAdmin():
    list_display = ['name', 'describe', 'work_year', 'address', 'concern_num',
                    'create_time', 'org']
    search_fields = ['name', 'describe', 'work_year', 'address', 'concern_num',
                     'create_time', 'org']
    list_filter = ['name', 'describe', 'work_year', 'address', 'concern_num',
                   'create_time', 'org__name']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)