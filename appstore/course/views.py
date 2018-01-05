from django.shortcuts import render, HttpResponse
from django.views.generic import View
from pure_pagination import Paginator, PageNotAnInteger
from course import models
from django.db.models import Q
from operation.models import UserFavorite, UserCourse, Comment
from utils.mixin_utils import LoginRequiredMixin
import json


# Create your views here.


# 课程列表页
class CourseListView(View):
    def get(self, request):
        all_courses = models.Course.objects.all().order_by("-create_time")
        hot_courses = models.Course.objects.all().order_by("-click_num")[:3]

        # 课程搜索
        serach_keywords = request.GET.get('keywords', "")
        if serach_keywords:
            all_courses = all_courses.filter(Q(name__icontains=serach_keywords) | Q(
                describe__icontains=serach_keywords) | Q(detail__icontains=serach_keywords))

        # 课程排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_num")

        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 3, request=request)

        courses = p.page(page)

        return render(request, 'course-list.html', {
            'all_courses': courses,
            'sort': sort,
            'hot_courses': hot_courses,

        })


# 课程详情页
class CourseDetailView(View):
    def get(self, request, course_id):
        course = models.Course.objects.get(nid=int(course_id))
        # 增加课程点击数
        course.click_num += 1
        course.save()

        has_fav_course = False
        has_fav_org = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(
                    user=request.user, fav_id=course_id, fav_type=1):
                has_fav_course = True

            if UserFavorite.objects.filter(
                    user=request.user,
                    fav_id=course.course_org.nid,
                    fav_type=2):
                has_fav_org = True
        # tag = course.tag
        # if tag:
        #     relate_courses = models.Course.objects.filter(tag=tag)[:1]
        # else:
        relate_courses = []

        return render(request, 'course-detail.html', {
            'course': course,
            "relate_courses": relate_courses,
            "has_fav_course": has_fav_course,
            "has_fav_org": has_fav_org,
        })


# 课程章节信息
class CourseInfoView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = models.Course.objects.get(nid=int(course_id))

        # 查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(
            user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
            course.students += 1
            course.save()

        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]

        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程 id
        course_ids = [
            user_course.course.nid for user_course in all_user_courses]
        # 获取学过该用户的学过的其他所有课程的前五名
        relate_courses = models.Course.objects.filter(
            nid__in=course_ids).order_by("-click_num")[:5]

        all_resource = models.CourseResouce.objects.filter(course=course)
        return render(request, 'course-video.html', {
            'course': course,
            'course_resources': all_resource,
            "relate_courses": relate_courses,
        })


# 课程评论
class CommentView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = models.Course.objects.get(nid=int(course_id))
        all_resources = models.CourseResouce.objects.filter(course=course)
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]

        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程 id
        course_ids = [
            user_course.course.nid for user_course in all_user_courses]
        # 获取学过该用户的学过的其他所有课程的前五名
        relate_courses = models.Course.objects.filter(
            nid__in=course_ids).order_by("-click_num")[:5]

        all_comments = Comment.objects.filter(course=course)
        return render(request, 'course-comment.html', {
            'course': course,
            'all_comments': all_comments,
            'all_resources': all_resources,
            "relate_courses": relate_courses,
        })


# 用户添加课程评论
class AddCommentView(View):
    def post(self, request):
        # 判断用户登录状态
        res = {}
        if not request.user.is_authenticated():
            res['status'] = False
            res['msg'] = '用户未登录'
            return HttpResponse(json.dumps(res))

        course_id = int(request.POST.get('course_id', 0))
        comments = request.POST.get('comments', '')
        if course_id and comments:
            course_comments = Comment()
            course_comments.course = models.Course.objects.get(nid=course_id)
            course_comments.content = comments
            course_comments.user = request.user
            course_comments.save()
            res['status'] = True
            res['msg'] = '添加成功'
        else:
            res['status'] = False
            res['msg'] = '添加失败'

        return HttpResponse(json.dumps(res))


# 视频播放页面
class VideoPlayView(LoginRequiredMixin, View):
    def get(self, request, vedio_id):
        video = models.Video.objects.get(id=int(vedio_id))
        course = video.lesson.course

        user_courses = UserCourse.objects.filter(
            user=request.user, course=course)
        if not user_courses:
            user_courses = UserCourse(user=request.user, course=course)
            user_courses.save()

        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [
            user_course.course.nid for user_course in all_user_courses]

        relate_courses = models.Course.objects.filter(
            nid__in=course_ids).order_by('-click_num')[:5]

        all_resources = models.CourseResouce.objects.filter(course=course)
        return render(request, 'course-play.html', {
            'course': course,
            'all_resources': all_resources,
            'relate_courses': relate_courses,
            'video': video,
        })
