from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login as dj_login, authenticate, logout
from django.views.generic.base import View
from .form import Loginform, RegisterForm, ForgetForm, ModifyPwdForm, UserInfoForm, UploadImageForm
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from . import models
from django.contrib.auth.hashers import make_password
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
import json
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from course.models import Course
from pure_pagination import Paginator, PageNotAnInteger
from django.core.urlresolvers import reverse


# Create your views here.


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = models.UserInfo.objects.get(
                Q(username=username) | Q(email=username))
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
                    return redirect(reverse("index"))
                else:
                    return render(
                        request, "login.html", {
                            "msg": "用户未激活", 'login_form': login_form})
            else:
                return render(
                    request, "login.html", {
                        "msg": "用户名或密码错误", 'login_form': login_form})
        else:
            return render(request, "login.html", {'login_form': login_form})


# 用户注销
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse("index"))


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(
            request, 'register.html', {
                'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            if models.UserInfo.objects.filter(email=user_name):
                return render(
                    request, 'register.html', {
                        'register_form': register_form, 'msg': '用户已经存在'})
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
            return render(
                request, 'register.html', {
                    'register_form': register_form})


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
            return render(
                request, 'forgetpwd.html', {
                    'forget_form': forget_form})


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
                return render(
                    request, 'password_reset.html', {
                        'msg': '密码不一致', 'email': email})
            else:
                user = models.UserInfo.objects.get(email=email)
                user.password = make_password(pwd2)
                user.save()
                return render(request, 'login.html')
        else:
            email = request.POST.get('email', '')
            return render(
                request, 'password_reset.html', {
                    'modify_form': modify_form, 'email': email})


def index(request):
    return render(request, 'index.html')


# 用户个人信息
class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        current_page = 'user_info'
        return render(request, 'usercenter-info.html', {
            'current_page': current_page,
        })

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        res = {}
        if user_info_form.is_valid():
            user_info_form.save()
            res['status'] = True
            return HttpResponse(json.dumps(res))
        else:
            return HttpResponse(json.dumps(user_info_form.errors))


# 在个人中心修改密码
class UpdataPwdView(LoginRequiredMixin, View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            res = {}
            if pwd1 != pwd2:
                res['status'] = False
                res['msg'] = "密码不一致"
                return HttpResponse(json.dumps(res))
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            res['status'] = True
            return HttpResponse(json.dumps(res))
        else:
            return HttpResponse(json.dumps(modify_form.errors))


# 用户修改头像
class UploadImageView(LoginRequiredMixin, View):
    def post(self, request):
        image_form = UploadImageForm(
            request.POST, request.FILES, instance=request.user)
        res = {}
        if image_form.is_valid():
            image_form.save()
            res['status'] = True
            # image = image_form.cleaned_data['avatar']
            # request.user.image = image
            # request.user.save()
        else:
            res['status'] = False
        return HttpResponse(json.dumps(res))


# 发送邮箱验证码
class SendEmailCodeView(LoginRequiredMixin, View):
    def get(self, request):
        email = request.GET.get('email', '')

        res = {}
        if models.UserInfo.objects.filter(email=email):
            res['email'] = '邮箱已注册'
            return HttpResponse(json.dumps(res))
        send_register_email(email, 'update_email')
        res['status'] = True
        res['email'] = '发送验证码成功'
        return HttpResponse(json.dumps(res))


# 修改个人邮箱
class UpdateEmailView(LoginRequiredMixin, View):
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        existed_records = models.EmailVerifyRecord.objects.filter(
            email=email, code=code, send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}')
        else:
            return HttpResponse('{"email":"验证码出错"}')


# 我的课程
class MycourseView(LoginRequiredMixin, View):
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        current_page = 'mycourse'
        return render(request, 'usercenter-mycourse.html', {
            "user_courses": user_courses,
            'current_page': current_page,
        })


# 我收藏的课程机构
class MyFavOrgView(LoginRequiredMixin, View):
    def get(self, request):
        org_list = []
        current_page = 'myfav_org'
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(nid=org_id)
            org_list.append(org)

        return render(request, 'usercenter-fav-org.html', {
            "org_list": org_list,
            'current_page': current_page,
        })


# 我收藏的授课讲师
class MyFavTeacherView(LoginRequiredMixin, View):
    def get(self, request):
        teacher_list = []
        current_page = 'myfav_org'
        fav_teachers = UserFavorite.objects.filter(
            user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(nid=teacher_id)
            teacher_list.append(teacher)

        return render(request, 'usercenter-fav-teacher.html', {
            "teacher_list": teacher_list,
            'current_page': current_page,
        })


# 我收藏的课程
class MyFavCourseView(LoginRequiredMixin, View):
    def get(self, request):
        course_list = []
        current_page = 'myfav_org'
        fav_courses = UserFavorite.objects.filter(
            user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(nid=course_id)
            course_list.append(course)

        return render(request, 'usercenter-fav-course.html', {
            "course_list": course_list,
            'current_page': current_page,
        })


# 我的消息
class MyMessageView(LoginRequiredMixin, View):
    def get(self, request):
        current_page = 'mymessage'
        all_message = UserMessage.objects.filter(user=request.user.id)

        # 用户进入个人消息后，清空未读消息的记录
        all_unread_messages = UserMessage.objects.filter(
            user=request.user.id, has_read=False)
        for unread_messages in all_unread_messages:
            unread_messages.has_read = True
            unread_messages.save()

        # 对个人消息进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_message, 1, request=request)

        messages = p.page(page)

        return render(request, 'usercenter-message.html', {
            "messages": messages,
            'current_page': current_page,
        })


class IndexView(View):
    def get(self, request):
        # 取出轮播图
        all_banners = models.Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            'all_banners': all_banners,
            'courses': courses,
            'banner_courses': banner_courses,
            'course_orgs': course_orgs,
        })


# 全局 404 处理函数
def page_not_found(request):
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


# 全局 404 处理函数
def page_error(request):
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
