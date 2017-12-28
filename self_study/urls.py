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


urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^login.html$', views.LoginView.as_view(), name="login"),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^register.html$', views.RegisterView.as_view(), name="register"),
    url(r'^index.html$', views.index, name='index'),
    url(r'^$', TemplateView.as_view(template_name="index.html"), name='index'),
]
