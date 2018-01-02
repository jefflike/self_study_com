# -*- coding:utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):
    '''
    用户未登录直接跳转到url
    '''
    @method_decorator(login_required(login_url='login.html'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)