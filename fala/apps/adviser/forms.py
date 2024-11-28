# coding=utf-8

from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.conf import settings
import laalaa.api as laalaa
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


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

    def clean(self):
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
                # stick the results of the valid api call into this
                self._country_from_valid_postcode = valid_postcode

        return data

    @property
    def region(self):
        # retrieve the api call variables
        country_from_valid_postcode = getattr(self, "_country_from_valid_postcode", None)

        # Return `Region.ENGLAND_OR_WALES` from `clean` if set
        if not country_from_valid_postcode:
            return getattr(self, "_region", None)

        # for Guernsey & Jersey the country comes back as 'Channel Islands', we are using `nhs_ha` key, to distinguish between them
        country, nhs_ha = country_from_valid_postcode

        if country == "Northern Ireland":
            return Region.NI
        elif country == "Isle of Man":
            return Region.IOM
        elif country == "Channel Islands" and nhs_ha == "Jersey Health Authority":
            return Region.JERSEY
        elif country == "Channel Islands" and nhs_ha == "Guernsey Health Authority":
            return Region.GUERNSEY
        elif country == "Scotland":
            return Region.SCOTLAND
        elif country == "England" or country == "Wales":
            return Region.ENGLAND_OR_WALES
        else:
            self.add_error("postcode", _("This service is only available for England and Wales"))
            return None

    @property
    def current_page(self):
        return self.cleaned_data.get("page", 1)

    def validate_postcode_and_return_country(self, postcode):
        try:
            # Check if the postcode is a valid string before proceeding
            if not isinstance(postcode, str) or not postcode.strip():
                return False

            # Retry set-up as per LAALAA API
            session = requests.Session()
            retry_strategy = Retry(total=5, backoff_factor=0.1)
            adapter = HTTPAdapter(max_retries=retry_strategy)
            session.mount("https://", adapter)

            # Call postcodes.io API using `api.postcodes.io/postcodes?q=` endpoint
            # This one let's you use partial postcodes and returns the country in the `result`
            url = settings.POSTCODE_IO_URL + f"{postcode}"
            response = session.get(url, timeout=5)

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
            self.add_error("postcode", _("Error looking up legal advisers. Please try again later."))
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


class SingleCategorySearchForm(forms.Form):
    postcode = CapitalisedPostcodeField(
        label=_("Postcode"),
        max_length=30,
        required=True,  # Postcode is required in this form
        widget=FalaTextInput(attrs={"class": "govuk-input govuk-!-width-two-thirds"}),
    )

    def __init__(self, categories=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure categories is a list and assign it to self.categories
        self.categories = categories if categories is not None else []

    def clean_postcode(self):
        postcode = self.cleaned_data.get("postcode")
        if not postcode:
            raise forms.ValidationError(_("Enter a valid postcode"))
        return postcode

    def clean(self):
        cleaned_data = super().clean()
        categories = self.data.get("category")
        if not categories:
            self.add_error("categories", "Category is required.")
        else:
            self.categories = [categories]
        return cleaned_data

    # this is required if i want to rename category to categories in the single_category_search.html file
    # however this then breaks the search as it just reloads the page

    def search(self):
        if self.is_valid():
            try:
                postcode = self.cleaned_data.get("postcode")
                if not postcode:
                    self.add_error("postcode", _("Enter a valid postcode"))
                    return {}

                # Use `self.categories` for the search (ensure it is passed as a list)
                data = laalaa.find(
                    postcode=postcode,
                    categories=self.categories,  # Pass the list of categories
                    page=1,  # Always default to the first page for simplicity
                )

                if "error" in data:
                    self.add_error("postcode", data["error"])
                    return {}
                return data

            except laalaa.LaaLaaError:
                self.add_error("postcode", _("Error looking up legal advisers. Please try again later."))
                return {}

        return {}
