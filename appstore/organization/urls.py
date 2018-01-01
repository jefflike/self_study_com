__author__ = 'Jeff'
__date__ = '2017/12/30 20:22'


from django.conf.urls import url
from organization import views


urlpatterns = [
    # 课程机构首页
    url(r'^list.html$', views.OrgView.as_view(), name='org_list'),
    url(r'^add_ask/$', views.AddUserAskView.as_view(), name='add_ask'),
    url(r'^home/(?P<org_id>\d+)/$', views.OrgHomeView.as_view(), name='org_home'),
    url(r'^course/(?P<org_id>\d+)/$', views.OrgCourseView.as_view(), name='org_course'),
    url(r'^desc/(?P<org_id>\d+)/$', views.OrgDescView.as_view(), name='org_desc'),
    url(r'^org_teacher/(?P<org_id>\d+)/$', views.OrgTeacherView.as_view(), name='org_teacher'),
    #
    url(r'^add_fav/$', views.AddFavView.as_view(), name='add_fav'),
    #
    # # 讲师列表页
    # url(r'^teacher/list/$', TeacherListView.as_view(), name='teacher_list'),
    #
    # # 讲师详情页
    # url(r'^teacher/detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name='teacher_detail'),

]