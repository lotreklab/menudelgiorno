import requests
import os
from django.contrib.auth import login
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from datetime import date
from app.models import Menu

from app.models import FirstCourse, SecondCourse, ContentMenu, SideCourse, Course

from web.models import SlackUser

CLIENT_ID = os.environ['SLACK_CLIENT_ID']
CLIENT_SECRET = os.environ['SLACK_CLIENT_SECRET']


def menu_view(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    first_courses = ContentMenu.objects.filter(menu=menu,
                                               course__polymorphic_ctype=ContentType.objects.get_for_model(FirstCourse))
    second_courses = ContentMenu.objects.filter(menu=menu, course__polymorphic_ctype=ContentType.objects.get_for_model(
        SecondCourse))
    side_courses = ContentMenu.objects.filter(menu=menu,
                                              course__polymorphic_ctype=ContentType.objects.get_for_model(SideCourse))
    return render(request, 'menu_view.html', {'menu': menu,
                                              'first': first_courses,
                                              'second': second_courses,
                                              'side': side_courses})


def course_view(request, pk):
    course = get_object_or_404(Course, pk=pk)
    repeat_count = ContentMenu.objects.filter(course=course).count()
    return render(request, 'course_view.html', {'course': course, 'count': repeat_count})


def menu_list(request):
    menu_today = Menu.objects.filter(consumeDate=date.today()).first()
    menu_data = Menu.objects.all().order_by('-consumeDate')
    page = request.GET.get('page', 1)
    paginator = Paginator(menu_data, 10)
    try:
        menus = paginator.page(page)
    except PageNotAnInteger:
        menus = paginator.page(1)
    except EmptyPage:
        menus = paginator.page(paginator.num_pages)

    return render(request, 'menu_list.html', {'menus': menus, 'menu_today': menu_today})


def login_view(request):
    token_response = requests.get("https://slack.com/api/oauth.access", params={
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': request.GET['code'],
        'request_uri': request.build_absolute_uri()
    }).json()
    if token_response['ok']:
        user = SlackUser.objects.update_or_create(slack_id=token_response['user']['id'],
                                                  username=token_response['user']['name'],
                                                  avatar=token_response['user']['image_72'],
                                                  access_token=token_response['access_token'])[0]
        login(request, user)
        return redirect(request.build_absolute_uri(request.GET['state']))
    else:
        return redirect(request.build_absolute_uri('/web'))
