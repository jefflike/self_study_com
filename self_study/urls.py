"""self_study URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from extra_apps import xadmin
from users import views
from django.views.generic import TemplateView
from django.views.static import serve
from self_study.settings import MEDIA_ROOT


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^login.html$', views.LoginView.as_view(), name="login"),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$',
        views.ActiveUserView.as_view(), name="active"),
    url(r'^reset/(?P<reset_code>.*)/$',
        views.ResetView.as_view(), name="reset_pwd"),
    url(r'^modify_pwd/$', views.ModifyPwdView.as_view(), name="modify_pwd"),
    url(r'^forget_pwd.html$', views.ForgetPwdView.as_view(), name="forget_pwd"),
    url(r'^register.html$', views.RegisterView.as_view(), name="register"),
    url(r'^index.html$', views.index),
    url(r'^$', views.IndexView.as_view(), name="index"),

    url(r'^org/', include('organization.urls', namespace='org')),
    url(r'^static/media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

    # 课程相关 url 配置
    url(r'^course/', include('course.urls', namespace='course')),

    # 用户相关 url 配置
    url(r'^users/', include('users.urls', namespace='users')),

    url(r'^logout/$', views.LogoutView.as_view(), name="logout"),
]

# 全局 404 页面配置
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'