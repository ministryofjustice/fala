# coding=utf-8

import re
from urllib.parse import urlparse, parse_qs, quote
from django_jinja import library
from jinja2 import pass_context


@library.filter
def url_to_human(value):
    return re.sub(r"(^https?://)|(/$)", "", value)


@library.filter
def human_to_url(value):
    return re.sub(r"^((?!https?://).*)", r"http://\1", quote(value))


@library.filter
@pass_context
def query_to_dict(_context, value, prop=None):
    result = parse_qs(urlparse(value).query)
    if not prop:
        return result

    return result.get(prop, [])


@library.filter
@pass_context
def to_fala_page_url(context, value, url_path):
    return "%s?%s" % (url_path, urlparse(value).query)


@library.filter
def google_map_params(item):
    organisation_type = item.get("type", "")
    organisation_name = item.get("organisation", {}).get("name", "")
    location = item.get("location", {})
    address = location.get("address", "")
    postcode = location.get("postcode", "")

    if "outreach" not in organisation_type.lower() and organisation_name:
        if postcode and address:
            return {"api": 1, "query": f"{organisation_name} {address} {postcode}"}
        elif address:
            return {"api": 1, "query": f"{organisation_name} {address}"}
        else:
            return {"api": 1, "query": f"{organisation_name} {postcode}"}
    elif postcode and address:
        return {"api": 1, "query": f"{address} {postcode}"}
    elif address:
        return {"api": 1, "query": address}
    else:
        return {"api": 1, "query": postcode}
