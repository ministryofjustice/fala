# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from .views import LocationSearchView, OrganisationSearchView

urlpatterns = [
    url(r'^$', LocationSearchView.as_view(), name='root'),
    url(r'^location/$', LocationSearchView.as_view(), name='location'),
    url(r'^organisation/$', OrganisationSearchView.as_view(), name='organisation'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG_STATIC:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    ]
