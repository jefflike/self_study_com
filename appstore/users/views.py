from django.shortcuts import render
from django.contrib.auth import login as dj_login, authenticate
from django.views.generic.base import View
from .form import Loginform, RegisterForm
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
                dj_login(request, user)
                return render(request, "index.html", {'user': user})
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
                user_info.password = make_password(pass_word)
                user_info.save()
            send_register_email(user_name,'register')
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'register_form': register_form})


def index(request):
    return render(request, 'index.html')


