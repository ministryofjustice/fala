# coding=utf-8
from urllib.parse import urlencode
from collections import OrderedDict
import requests
import logging

from django.conf import settings
from django.utils.translation import gettext_lazy as _

from cla_common.laalaa import LaalaaProviderCategoriesApiClient, LaaLaaError

try:
    basestring
except NameError:
    basestring = str

logger = logging.getLogger(__name__)
def get_categories():
    if settings.LAALAA_API_HOST:
        categories = LaalaaProviderCategoriesApiClient.singleton(settings.LAALAA_API_HOST, _).get_categories()
        # sort by name (the second item in the tuple) rather than the code
        return [item for item in sorted(categories.items(), key=lambda x: x[1])]

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
    try:
        response = requests.get(laalaa_url(**kwargs))
        return response.json()
    except (requests.exceptions.RequestException, ValueError) as e:
        raise LaaLaaError(e)


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

    data["results"] = list(map(decode_categories, data.get("results", [])))
    logger.debug(f"find: processed results type={type(data['results'])}, processed results={data['results'][:3]}")  # Log first 3 processed results

    return data
