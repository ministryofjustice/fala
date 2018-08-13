# -*- coding: utf-8 -*-

import re
from urllib.parse import urlparse, parse_qs, quote
from django_jinja import library
from jinja2 import contextfilter


@library.filter
def url_to_human(value):
    return re.sub(r'(^https?://)|(/$)', '', value)


@library.filter
def human_to_url(value):
    return re.sub(r'^((?!https?://).*)', r'http://\1', quote(value))


@library.filter
@contextfilter
def query_to_dict(_context, value, prop=None):
    result = parse_qs(urlparse(value).query)
    if not prop:
        return result

    return result.get(prop, [])


@library.filter
@contextfilter
def to_fala_page_url(context, value, url_path):
    return '%s?%s' % (url_path, urlparse(value).query)
