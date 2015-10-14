# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import LocationSearchView, OrganisationSearchView

urlpatterns = [
    url(r'^$', LocationSearchView.as_view(), name='root'),
    url(r'^location/$', LocationSearchView.as_view(), name='location'),
    url(r'^organisation/$', OrganisationSearchView.as_view(), name='organisation'),
]
