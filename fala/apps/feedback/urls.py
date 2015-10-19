# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import FeedbackView, FeedbackConfirmationView

urlpatterns = [
    url(r'^feedback/$', FeedbackView.as_view(), name='feedback'),
    url(r'^feedback/success$', FeedbackConfirmationView.as_view(), name='feedback_confirmation'),
]
