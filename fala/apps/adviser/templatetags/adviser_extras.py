# -*- coding: utf-8 -*-

from django_jinja import library
from jinja2 import contextfilter
from urllib.parse import urlparse, parse_qs


@library.filter
def multiply(value, arg):
    return value * arg

@library.filter
def val(field):
    return field.value() if field.value() else ''

@library.filter
@contextfilter
def query_to_dict(context, value, prop=None):
    result = parse_qs(urlparse(value).query)
    if prop:
        result = result[prop]
    return result


@library.filter
@contextfilter
def to_fala_page_url(context, value, url_path):
    return '%s?%s' % (url_path, urlparse(value).query)

