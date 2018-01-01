from django.shortcuts import render, HttpResponse
from django.views.generic.base import View
from organization import models
from pure_pagination import Paginator, PageNotAnInteger
import json
from .form import UserAskForm
from course.models import Course
from operation.models import UserFavorite


# Create your views here.


class OrgView(View):
    def get(self, request):
        all_citys = models.CityDict.objects.all()
        all_orgs = models.CourseOrg.objects.all()
        all_cate = models.CourseOrg.choices

        # 提取热门机构
        hot_orgs = all_orgs.order_by("-click_num")[:3]

        # 类别筛选
        categorys = request.GET.get('ct', "")
        if categorys:
            # 筛选出当前城市的结果集
            all_orgs = all_orgs.filter(category=categorys)

        # 取出筛选城市
        city_id = request.GET.get('city', "")
        if city_id:
            # 筛选出当前城市的结果集
            all_orgs = all_orgs.filter(city_id=int(city_id))

        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-courses_nums")

        all_count = all_orgs.count()
        try:
            page = request.GET.get('page', 1)  # 获取当前页码,如果没有默认1
        except PageNotAnInteger:  # 如果获取页码出错，默认1
            page = 1

        p = Paginator(all_orgs, 1, request=request)  # 执行分页函数，参数1数据库的数据，参数2显示多少条数据，参数3request
        orgs_page = p.page(page)  # 返回一个，包含了分页数据和分页导航的对象
        return render(request, 'org-list.html', {'all_citys': all_citys, 'all_orgs': orgs_page, 'all_cate': all_cate,
                                                 'all_count': all_count, 'city_id': city_id, 'categorys': categorys,
                                                 'hot_orgs': hot_orgs, 'sort': sort})


class AddUserAskView(View):
    def post(self, request):
        user_ask_form = UserAskForm(request.POST)
        res = {}
        if user_ask_form.is_valid():
            user_ask_form.save(commit=True)
            res['status'] = True
        else:
            res['status'] = False
            res['msg'] = '添加出错'
        return HttpResponse(json.dumps(res))


class OrgHomeView(View):
    def get(self, request, org_id):
        course_org = models.CourseOrg.objects.filter(nid=org_id).first()
        all_courses = Course.objects.filter(course_org=course_org)
        all_teacher = models.Teacher.objects.filter(org=course_org)
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.nid, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-homepage.html', {'course_org': course_org, 'all_courses': all_courses,
                                                            'all_teacher': all_teacher, 'has_fav': has_fav})


class OrgCourseView(View):
    def get(self, request, org_id):
        course_org = models.CourseOrg.objects.filter(nid=org_id).first()
        current_page = "course"
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.nid, fav_type=2):
                has_fav = True
        # 有外键的地方都可以这样用，通过外键取出数据
        all_courses = Course.objects.filter(course_org=course_org)
        try:
            page = request.GET.get('page', 1)  # 获取当前页码,如果没有默认1
        except PageNotAnInteger:  # 如果获取页码出错，默认1
            page = 1

        p = Paginator(all_courses, 1, request=request)  # 执行分页函数，参数1数据库的数据，参数2显示多少条数据，参数3request
        orgs_page = p.page(page)  # 返回一个，包含了分页数据和分页导航的对象
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
            'orgs_page': orgs_page,
        })


# 机构介绍页
class OrgDescView(View):
    def get(self, request, org_id):
        course_org = models.CourseOrg.objects.filter(nid=org_id).first()
        current_page = "desc"
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.nid, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgTeacherView(View):
    def get(self, request, org_id):
        course_org = models.CourseOrg.objects.filter(nid=org_id).first()
        current_page = "teacher"
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.nid, fav_type=2):
                has_fav = True

        # 有外键的地方都可以这样用，通过外键取出数据
        all_teachers = models.Teacher.objects.filter(org=course_org)
        return render(request, 'org-detail-teachers.html', {
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class AddFavView(View):
    def post(self, request):
        fav_id = int(request.POST.get('fav_id', 0))
        fav_type = int(request.POST.get('fav_type', 0))
        res = {}
        if not request.user.is_authenticated():
            res['status'] = False
            res['msg'] = '用户未登录'
            return HttpResponse(json.dumps(res))
        # 查询收藏记录
        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)
        if exist_records:
            exist_records.delete()
            res['status'] = True
            res['msg'] = '收藏'
        else:
            user_fav = UserFavorite()
            if fav_id and fav_type:
                user_fav.user = request.user
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.save()
                res['status'] = True
                res['msg'] = '已收藏'
            else:
                res['status'] = False
                res['msg'] = '收藏出错'
        return HttpResponse(json.dumps(res))