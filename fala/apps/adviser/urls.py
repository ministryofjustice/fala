# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import IndexView

urlpatterns = [
    url(r'^$', IndexView.as_view()),
]
