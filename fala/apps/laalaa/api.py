# coding=utf-8
from urllib.parse import urlencode
from collections import OrderedDict
import requests

from django.conf import settings
from django.utils.translation import gettext_lazy as _

from cla_common.laalaa import LaalaaProviderCategoriesApiClient, LaaLaaError

try:
    basestring
except NameError:
    basestring = str


def return_get_categories():
   return [
    {
        "code": "MOSL",
        "civil": True,
        "name": "Modern slavery"
    },
    {
        "code": "MED",
        "civil": True,
        "name": "Clinical negligence"
    },
    {
        "code": "PUB",
        "civil": True,
        "name": "Public law"
    },
    {
        "code": "MHE",
        "civil": True,
        "name": "Mental health"
    },
    {
        "code": "COM",
        "civil": True,
        "name": "Community care"
    },
    {
        "code": "DEB",
        "civil": True,
        "name": "Debt"
    },
    {
        "code": "WB",
        "civil": True,
        "name": "Welfare benefits"
    },
    {
        "code": "HLPAS",
        "civil": True,
        "name": "Housing Loss Prevention Advice Service"
    },
    {
        "code": "FMED",
        "civil": True,
        "name": "Family mediation"
    },
    {
        "code": "DISC",
        "civil": True,
        "name": "Discrimination"
    },
    {
        "code": "AAP",
        "civil": True,
        "name": "Claims Against Public Authorities"
    },
    {
        "code": "EDU",
        "civil": True,
        "name": "Education"
    },
    {
        "code": "MAT",
        "civil": True,
        "name": "Family"
    },
    {
        "code": "IMMAS",
        "civil": True,
        "name": "Immigration or asylum"
    },
    {
        "code": "HOU",
        "civil": True,
        "name": "Housing"
    },
    {
        "code": "PL",
        "civil": False,
        "name": "Prison law"
    },
    {
        "code": "CRM",
        "civil": False,
        "name": "Crime"
    }
]



def get_categories():
    categories = return_get_categories()
    return [item for item in sorted(categories.items(), key=lambda x: x[1])]




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
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return response.json()
        raise LaaLaaError(e)
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

    # because of the way the current error capture and forms are set up, it is
    # easier to allow the 404 errors through as a valid response and treat them separately.
    if "error" in data:
        return data
    else:
        data["results"] = list(map(decode_categories, data.get("results", [])))
        return data
