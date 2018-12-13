# coding=utf-8
from urllib.parse import urlencode
from collections import OrderedDict
import requests

try:
    from django.conf import settings
    from django.utils.translation import gettext_lazy as _

    LAALAA_API_HOST = settings.LAALAA_API_HOST
except ImportError:
    from flask import current_app
    from flask.ext.babel import lazy_gettext as _

    LAALAA_API_HOST = current_app.config["LAALAA_API_HOST"]

try:
    basestring
except NameError:
    basestring = str

PROVIDER_CATEGORY_CHOICES = (
    ("aap", _("Actions against the police")),
    ("med", _("Clinical negligence")),
    ("com", _("Community care")),
    ("crm", _("Crime")),
    ("deb", _("Debt")),
    ("mat", _("Family")),
    ("fmed", _("Family mediation")),
    ("hou", _("Housing")),
    ("immas", _("Immigration or asylum")),
    ("mhe", _("Mental health")),
    ("pl", _("Prison law")),
    ("pub", _("Public law")),
    ("wb", _("Welfare benefits")),
)

PROVIDER_CATEGORIES = OrderedDict(PROVIDER_CATEGORY_CHOICES)


class LaaLaaError(Exception):
    pass


def kwargs_to_urlparams(**kwargs):
    kwargs = dict(filter(lambda kwarg: kwarg[1], kwargs.items()))
    return urlencode(kwargs, True)


def laalaa_url(**kwargs):
    return "{host}/legal-advisers/?{params}".format(host=LAALAA_API_HOST, params=kwargs_to_urlparams(**kwargs))


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

    return data
