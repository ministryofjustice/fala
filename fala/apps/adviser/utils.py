# utils.py

from fala.apps.constants.categories import CATEGORY_TRANSLATIONS
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from django.conf import settings
from django.utils.translation import gettext_lazy as _


def validate_postcode_and_return_country(postcode, form=None):
    try:
        if not isinstance(postcode, str) or not postcode.strip():
            return False

        session = requests.Session()
        retry_strategy = Retry(total=5, backoff_factor=0.1)
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)

        url = settings.POSTCODE_IO_URL + f"{postcode}"
        response = session.get(url, timeout=5)

        if response.status_code != 200:
            return False

        data = response.json()

        if not data.get("result"):
            return False

        first_result_in_list = data["result"][0]
        country = first_result_in_list.get("country")
        nhs_ha = first_result_in_list.get("nhs_ha")

        if country and nhs_ha:
            return country, nhs_ha
        else:
            return False

    except requests.RequestException:
        if form:
            form.add_error("postcode", _("Error looking up legal advisers. Please try again later."))
        return False

SLUG_TO_CODE = {display_name: category_code for category_code, display_name in CATEGORY_TRANSLATIONS.items()}


def get_category_code_from_slug(slug):
    return SLUG_TO_CODE.get(slug)


def get_category_display_name(category_code):
    return CATEGORY_TRANSLATIONS.get(category_code)


CATEGORY_MESSAGES = {
    "hlpas": "Tell the adviser your home is at risk and you want advice through the Housing Loss Prevention Advice Service.",
    "welfare-benefits": (
        "Legal aid for advice about welfare benefits is only available if you are appealing a decision made by the social security tribunal. "
        "This appeal must be in the Upper Tribunal, Court of Appeal or Supreme Court.\n\n"
        "For any other benefits issue, ask the legal adviser if you can get free legal advice or if you will have to pay for it."
    ),
    "clinical-negligence": "Legal aid for advice about clinical negligence is usually only available if you have a child that suffered a brain injury during pregnancy, birth or the first 8 weeks of life.",
}

CATEGORY_DISPLAY_NAMES = {
    "hlpas": "Housing Loss Prevention Advice Service",
}

