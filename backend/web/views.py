import requests
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from app.models import Menu

from app.models import FirstCourse, SecondCourse, ContentMenu, SideCourse, Course


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
    menu_data = Menu.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(menu_data, 10)
    try:
        menus = paginator.page(page)
    except PageNotAnInteger:
        menus = paginator.page(1)
    except EmptyPage:
        menus = paginator.page(paginator.num_pages)

    return render(request, 'menu_list.html', {'menus': menus})
