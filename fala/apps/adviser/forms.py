# coding=utf-8

from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.conf import settings

import laalaa.api as laalaa
import requests

from .regions import Region

SEARCH_TYPE_CHOICES = [("location", _("Location")), ("organisation", _("Organisation"))]

ORGANISATION_TYPES_CHOICES = [
    ("Charity or Voluntary Org", "Charity or Voluntary Organisations"),
    ("Mediation", "Mediation Service"),
    ("Private Company", "Private Company"),
    ("Solicitor", "Solicitor"),
]


class FalaTextInput(forms.TextInput):
    def __init__(self, attrs={}):
        class_attr = " ".join([c for c in ["govuk-input govuk-!-width-one-third", attrs.get("class")] if c])
        attrs.update({"class": class_attr})

        super(FalaTextInput, self).__init__(attrs)


class CapitalisedPostcodeField(forms.CharField):
    # converting String representation into a Python object
    def to_python(self, value):
        # Capitalise the input value
        capitalised_value = value.upper() if value else value
        return super().to_python(capitalised_value)


# This is so that we can hit the front page with query parameters in url and not see form validation errors
# In django, form validation happens when the data is cleaned, i.e. form validation, form errors, form cleaned
# `def clean(self)` is the method triggering form validation, so have extracted that into `AdviserSearchForm` form class
class AdviserRootForm(forms.Form):
    postcode = CapitalisedPostcodeField(
        label=_("Postcode"),
        max_length=30,
        help_text=_(mark_safe("For example, <span class='notranslate' translate='no'>NE31 1SF</span>")),
        required=False,
        widget=FalaTextInput(),
    )

    name = forms.CharField(
        label=_("Organisation name"),
        max_length=100,
        required=False,
        widget=FalaTextInput(),
    )

    categories = forms.MultipleChoiceField(
        label=_("Category"),
        choices=laalaa.PROVIDER_CATEGORY_CHOICES,
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )


class AdviserSearchForm(AdviserRootForm):
    page = forms.IntegerField(required=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("label_suffix", "")
        super(AdviserRootForm, self).__init__(*args, **kwargs)

    def clean(self):  # noqa: max-complexity=13 (increasing the complexity of a function so flake8 is happy)
        data = self.cleaned_data
        postcode = data.get("postcode")
        name = data.get("name")

        # Add error if both postcode and name are missing
        if not postcode and not name:
            self.add_error("postcode", _("Enter a postcode"))
            self.add_error("name", _("Enter an organisation name"))
            return data

        # Do search on organisation name even if postcode missing
        if not postcode and name:
            self._region = Region.ENGLAND_OR_WALES
            return data

        # Validate postcode if provided and then determine region
        if postcode:
            valid_postcode = self.validate_postcode_and_return_country(postcode)
            if not valid_postcode:
                self.add_error("postcode", _("Enter a valid postcode"))
            else:
                # for Guernsey & Jersey the country comes back as 'Channel Islands', we are using `nhs_ha` key, to distinguish between them
                country, nhs_ha = valid_postcode
                if country == "Northern Ireland":
                    self._region = Region.NI
                elif country == "Isle of Man":
                    self._region = Region.IOM
                elif country == "Channel Islands" and nhs_ha == "Jersey Health Authority":
                    self._region = Region.JERSEY
                elif country == "Channel Islands" and nhs_ha == "Guernsey Health Authority":
                    self._region = Region.GUERNSEY
                elif country == "Scotland":
                    self._region = Region.SCOTLAND
                elif country == "England" or country == "Wales":
                    self._region = Region.ENGLAND_OR_WALES
                else:
                    self.add_error("postcode", _("This service is only available for England and Wales"))

        return data

    @property
    def region(self):
        # If no region was detected, return None.
        return getattr(self, "_region", None)

    @property
    def current_page(self):
        return self.cleaned_data.get("page", 1)

    def validate_postcode_and_return_country(self, postcode):
        try:
            # Check if the postcode is a valid string before proceeding
            if not isinstance(postcode, str) or not postcode.strip():
                return False

            # Call postcodes.io API using `api.postcodes.io/postcodes?q=` endpoint
            # This one let's you use partial postcodes and returns the country in the `result`
            url = settings.POSTCODE_IO_URL + f"{postcode}"
            response = requests.get(url)

            # Check if response was successful
            if response.status_code != 200:
                return False

            # If the 'result' key is Null, the postcode is invalid
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
            # If there is an exception from postcode.io, tell the user there was an error, but don't stop the usage of the site.
            self.add_error("postcode", _("Error looking up legal advisers via our API. Please try again later."))
            return False

    def search(self):
        if self.is_valid():
            try:
                data = laalaa.find(
                    postcode=self.cleaned_data.get("postcode"),
                    categories=self.cleaned_data.get("categories"),
                    page=self.cleaned_data.get("page", 1),
                    organisation_types=self.cleaned_data.get("type"),
                    organisation_name=self.cleaned_data.get("name"),
                )
                if "error" in data:
                    self.add_error("postcode", (data["error"]))
                    return {}
                return data
            except laalaa.LaaLaaError:
                self.add_error(
                    "postcode", "%s %s" % (_("Error looking up legal advisers."), _("Please try again later."))
                )
                return {}
        else:
            return {}
