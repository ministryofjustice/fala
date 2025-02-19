# coding=utf-8

import re
from urllib.parse import urlparse, parse_qs, quote
from django_jinja import library
from jinja2 import pass_context
from laalaa.api import PROVIDER_CATEGORIES


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
    organisation_name = item.get("organisation", {}).get("name", "")
    location = item.get("location", {})
    office_type = location.get("type", "")
    address = location.get("address", "")
    postcode = location.get("postcode", "")

    if "outreach" not in office_type.lower() and organisation_name:
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


@library.filter
def category_selection(form):
    if "categories" in form.cleaned_data:
        categories = [PROVIDER_CATEGORIES[cat] for cat in form.cleaned_data["categories"]]
        formatted_categories = ", ".join(map(str, categories))

        return formatted_categories
    return None


@library.filter
def category_selection_first_item(form):
    categories = form.cleaned_data.get("categories", [])

    if categories:
        return PROVIDER_CATEGORIES.get(categories[0], None)

    return None


@library.filter
def category_selection_list(form):
    if "categories" in form.cleaned_data:
        categories = [PROVIDER_CATEGORIES[cat] for cat in form.cleaned_data["categories"]]
        return map(str, categories)
    return []


@library.filter
def form_categories(categories):
    processed_categories = []
    for value, text in categories.field.choices:
        if text == "Claims Against Public Authorities":
            text = "Claims against public authorities"
        processed_categories.append({"value": value, "text": text, "id": f"id_categories_{text}"})
    return processed_categories
