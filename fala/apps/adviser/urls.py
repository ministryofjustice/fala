# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from .views import LocationSearchView, OrganisationSearchView

urlpatterns = [
    url(r'^$', LocationSearchView.as_view()),
    url(r'^location/$', LocationSearchView.as_view()),
    url(r'^organisation/$', OrganisationSearchView.as_view()),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
