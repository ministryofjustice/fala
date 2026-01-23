# coding=utf-8
from urllib.parse import urlencode
from collections import OrderedDict
from django.conf import settings
import json

try:
    basestring
except NameError:
    basestring = str


def load_data(file_path: str) -> json:
    with open(file_path, "r") as apiData:
        data = json.load(apiData)

    return data if data else []


def get_categories():
    if settings.LAALAA_API_HOST:
        data = load_data(file_path="mock_api_categories.json")
        if not data:
            raise FileNotFoundError("Not able to locate the mock Json File")

        return [item for item in sorted(data.items(), key=lambda x: x[1])]

    return []


PROVIDER_CATEGORY_CHOICES = get_categories()
PROVIDER_CATEGORIES = OrderedDict(PROVIDER_CATEGORY_CHOICES)


def kwargs_to_urlparams(**kwargs):
    kwargs = dict(filter(lambda kwarg: kwarg[1], kwargs.items()))
    return urlencode(kwargs, True)


def laalaa_url(**kwargs):
    return "{host}/legal-advisers/?{params}".format(
        host=settings.LAALAA_API_HOST, params=kwargs_to_urlparams(**kwargs)
    )


def laalaa_search(**kwargs):
    data = load_data(file_path="mock_api_categories.json")

    return data if data else FileNotFoundError("Not able to locate the mock Json File")


def decode_category(category):
    if category and isinstance(category, basestring):
        return PROVIDER_CATEGORIES.get(category.lower())


def decode_categories(result):
    result["categories"] = list(filter(None, map(decode_category, result.get("categories", []))))
    return result


def find(postcode=None, categories=None, page=1, organisation_types=None, organisation_name=None):
    data = laalaa_search(
        postcode=postcode,
        categories=categories,
        page=page,
        organisation_types=organisation_types,
        organisation_name=organisation_name,
    )

    # because of the way the current error capture and forms are set up, it is
    # easier to allow the 404 errors through as a valid response and treat them separately.
    if "error" in data:
        return data
    else:
        data["results"] = list(map(decode_categories, data.get("results", [])))
        return data
