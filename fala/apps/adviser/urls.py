# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from .views import IndexView

urlpatterns = [
    url(r'^$', IndexView.as_view()),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
