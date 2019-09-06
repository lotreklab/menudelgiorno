import json
import re

import requests
from redis import Redis
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from app import serializers

from app.models import Course, Menu, ContentMenu


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = serializers.CoursePolymorphicSerializer

    @action(detail=True, methods=['get'])
    def image_search(self, request, pk=None):
        redis_connection = Redis()
        course = self.get_object()

        search_result = redis_connection.get(hash(course))
        if not search_result:
            search_string = str(course)
            search_token = re.findall(r'vqd=\'(.*)\';',
                                      requests.post("https://duckduckgo.com/", data={'q': search_string}).text)[0]
            search_result = requests.get("https://duckduckgo.com/i.js?l=it-it&o=json&vqd=%s&q=%s&f=,,,&p=2" % (search_token, search_string),
                                         headers={
                                             'Dnt': '1',
                                             'X-Requested-With': 'XMLHttpRequest',
                                             'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
                                             'Accept': 'application/json, text/javascript, */*; q=0.01',
                                             'Referer': 'https://duckduckgo.com/',
                                             'Authority': 'duckduckgo.com',
                                             'Host': 'duckduckgo.com',
                                             'Connection': 'keep-alive',
                                             'Cache-Control': 'no-cache',
                                         }).text
            redis_connection.append(hash(course), search_result)
        redis_connection.close()
        return Response(json.loads(search_result)['results'][0])

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = serializers.MenuSerializer

class ContentMenuViewSet(viewsets.ModelViewSet):
    queryset = ContentMenu.objects.all()
    serializer_class = serializers.ContentMenuSerializer
