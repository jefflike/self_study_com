from django.shortcuts import render,HttpResponse
from django.contrib.auth import login as dj_login, authenticate
from django.views.generic.base import View
from .form import Loginform, RegisterForm, ForgetForm, ModifyPwdForm
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from . import models
from django.contrib.auth.hashers import make_password
from utils.email_send import send_register_email


# Create your views here.


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = models.UserInfo.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = Loginform(request, request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    dj_login(request, user)
                    return render(request, "index.html", {'user': user})
                else:
                    return render(request, "login.html", {"msg": "用户未激活", 'login_form': login_form})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误", 'login_form': login_form})
        else:
            return render(request, "login.html", {'login_form': login_form})


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            if models.UserInfo.objects.filter(email=user_name):
                return render(request, 'register.html', {'register_form': register_form, 'msg': '用户已经存在'})
            else:
                pass_word = request.POST.get('password', '')
                user_info = models.UserInfo()
                user_info.username = user_name
                user_info.email = user_name
                user_info.is_active = False
                user_info.password = make_password(pass_word)
                user_info.save()
            send_register_email(user_name, 'register')
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'register_form': register_form})


class ActiveUserView(View):
    def get(self, request, active_code):
        all_record = models.EmailVerifyRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                email = record.email
                user = models.UserInfo.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return HttpResponse('<h1>链接失效</h1>')
        return render(request, 'login.html')


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_register_email(email, 'forget')
            return HttpResponse('<h1>邮件已发送，注意查收</h1>')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetView(View):
    def get(self, request, reset_code):
        all_record = models.EmailVerifyRecord.objects.filter(code=reset_code)
        if all_record:
            for record in all_record:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})
        else:
            return HttpResponse('<h1>链接失效</h1>')
        return render(request, 'login.html')


class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'msg': '密码不一致', 'email': email})
            else:
                user = models.UserInfo.objects.get(email=email)
                user.password = make_password(pwd2)
                user.save()
                return render(request, 'login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'modify_form': modify_form, 'email': email})


def index(request):
    return render(request, 'index.html')


