# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import FeedbackView

urlpatterns = [
    url(r'^feedback/$', FeedbackView.as_view(), name='feedback'),
]
