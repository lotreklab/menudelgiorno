from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path(r'menu/<int:pk>/', views.menu_view, name='menu_view'),
    path(r'course/<int:pk>/', views.course_view, name='course_view'),
    path(r'', views.menu_list, name='menu_list'),
    path(r'login', views.login_view, name='login')
]