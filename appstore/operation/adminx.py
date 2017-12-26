__author__ = 'Jeff'
__date__ = '2017/12/26 12:36'

from extra_apps import xadmin
from .models import UserAsk, Comment, UserFavorite, UserMessage, UserCourse


class UserAskAdmin():
    list_display = ['name', 'mobile', 'course_name', 'create_time']
    search_fields = ['name', 'mobile', 'course_name']
    list_filter = ['name', 'mobile', 'course_name', 'create_time']


class CommentAdmin():
    list_display = ['user', 'course', 'content', 'create_time']
    search_fields = ['user', 'course', 'content']
    list_filter = ['user__username', 'course__name', 'content', 'create_time']


class UserFavoriteAdmin():
    list_display = ['user', 'fav_id', 'fav_type', 'create_time']
    search_fields = ['user', 'fav_id', 'fav_type']
    list_filter = ['user__username', 'fav_id', 'fav_type', 'create_time']


class UserMessageAdmin():
    list_display = ['user', 'message', 'has_read', 'create_time']
    search_fields = ['user', 'message', 'has_read']
    list_filter = ['user', 'message', 'has_read', 'create_time']


class UserCourseAdmin():
    list_display = ['user', 'course', 'create_time']
    search_fields = ['user', 'course']
    list_filter = ['user__username', 'course__name', 'create_time']


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(Comment, CommentAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)