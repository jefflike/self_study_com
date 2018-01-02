__author__ = 'Jeff'
__date__ = '2018/1/1 11:43'


from django.conf.urls import url
from course import views


urlpatterns = [
    # 课程列表页
    url(r'^list/$', views.CourseListView.as_view(), name='course_list'),

    # # 课程详情页
    url(r'^detail/(?P<course_id>\d+)/$', views.CourseDetailView.as_view(), name='course_detail'),
    # 
    # # 课程信息页
    url(r'^info/(?P<course_id>\d+)/$', views.CourseInfoView.as_view(), name='course_info'),
    # 
    # # 课程评论页
    url(r'^comment/(?P<course_id>\d+)/$', views.CommentView.as_view(), name='course_comment'),
    # 
    # # 添加课程评论
    url(r'^add_comment/$', views.AddCommentView.as_view(), name='add_comment'),
    # 
    # # 添加课程评论
    url(r'^vedio/(?P<vedio_id>\d+)/$', views.VideoPlayView.as_view(), name='vedio_play'),
]