from django.conf.urls import url
from users import views


urlpatterns = [
    # 用户信息
    url(r'^info/$', views.UserInfoView.as_view(), name='user_info'),

    # 用户信息
    url(r'^image/upload/$', views.UploadImageView.as_view(), name='image_upload'),

    # # 用户个人中心修改密码
    url(r'^update/pwd/$', views.UpdataPwdView.as_view(), name='update_pwd'),
    #
    # # 发送邮箱验证码
    url(r'^sendemail_code/$', views.SendEmailCodeView.as_view(), name='sendemail_code'),
    #
    # # 修改邮箱
    url(r'^update_email/$', views.UpdateEmailView.as_view(), name='update_email'),
    #
    # # 我的课程
    url(r'^mycourse/$', views.MycourseView.as_view(), name='mycourse'),
    #
    # # 我收藏的课程机构
    url(r'^myfav/org/$', views.MyFavOrgView.as_view(), name='myfav_org'),
    #
    # # 我收藏的授课讲师
    url(r'^myfav/teacher/$', views.MyFavTeacherView.as_view(), name='myfav_teacher'),
    #
    # # 我收藏的课程
    url(r'^myfav/course/$', views.MyFavCourseView.as_view(), name='myfav_course'),
    #
    # # 我的消息
    url(r'^mymessage/$', views.MyMessageView.as_view(), name='mymessage'),

]