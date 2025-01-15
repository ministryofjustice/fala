# utils.py
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
