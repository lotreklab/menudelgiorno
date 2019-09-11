import requests
import os
from django.contrib.auth import login
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from datetime import date

from app.models import FirstCourse, SecondCourse, ContentMenu, SideCourse, Course, Menu

from web.models import SlackUser, Review

from web.forms import ReviewForm

CLIENT_ID = os.environ['SLACK_CLIENT_ID']
CLIENT_SECRET = os.environ['SLACK_CLIENT_SECRET']


def menu_view(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    first_courses = ContentMenu.objects.filter(menu=menu,
                                               course__polymorphic_ctype=ContentType.objects.get_for_model(FirstCourse))
    second_courses = ContentMenu.objects.filter(menu=menu,
                                                course__polymorphic_ctype=ContentType.objects.get_for_model(SecondCourse))
    side_courses = ContentMenu.objects.filter(menu=menu,
                                              course__polymorphic_ctype=ContentType.objects.get_for_model(SideCourse))
    return render(request, 'menu_view.html', {'menu': menu,
                                              'first': first_courses,
                                              'second': second_courses,
                                              'side': side_courses})


def course_view(request, pk):
    course = get_object_or_404(Course, pk=pk)
    repeat_count = ContentMenu.objects.filter(course=course).count()
    if request.user.is_authenticated:
        reviews = list(Review.objects.filter(course=course, user=request.user)) + list(Review.objects.filter(course=course).exclude(user=request.user))
    else:
        reviews = list(Review.objects.filter(course=course))
    return render(request, 'course_view.html', {'course': course,
                                                'count': repeat_count,
                                                'reviews': reviews,
                                                'user_has_reviewed': request.user.is_authenticated and Review.objects.filter(user=request.user, course=course).count() == 1})


def menu_list(request):
    menu_today = Menu.objects.filter(consume_date=date.today()).first()
    menu_data = Menu.objects.all().order_by('-consume_date')
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
        'redirect_uri': request.build_absolute_uri(request.path)
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


def review_view(request, course):
    course = get_object_or_404(Course, pk=course)
    review = Review.objects.filter(user=request.user, course=course)
    form = ReviewForm(instance=review[0]) if review else ReviewForm({'text':''})
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if "remove" in request.POST.keys():
            Review.objects.filter(user=request.user, course=course).delete()
            return redirect(request.build_absolute_uri('/web/course/%d' % course.id))
        elif form.is_valid():
            review = form.save(commit=False)
            Review.objects.update_or_create(user=request.user, course=course, defaults={
                'score': review.score,
                'text': review.text
            })
            return redirect(request.build_absolute_uri('/web/course/%d' % course.id))
    return render(request, 'review_view.html', {'form': form, 'course': course, 'is_edit': bool(review)})
