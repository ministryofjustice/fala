# coding=utf-8

from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from .regions import Region
from fala.apps.adviser.utils import validate_postcode_and_return_country
import laalaa.api as laalaa


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


class BaseSearch:
    def perform_search(self, form, postcode, categories, page):
        try:
            data = laalaa.find(
                postcode=postcode,
                categories=categories,
                page=page,
                organisation_types=form.cleaned_data.get("type"),
                organisation_name=form.cleaned_data.get("name"),
            )
            if "error" in data:
                form.add_error("postcode", data["error"])
            return data
        except laalaa.LaaLaaError:
            form.add_error("postcode", "%s %s" % (_("Error looking up legal advisers."), _("Please try again later.")))
            return {}

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


class AdviserSearchForm(AdviserRootForm, BaseSearch):
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
    def current_page(self):
        return self.cleaned_data.get("page", 1)

    def validate_postcode_and_return_country(self, postcode):
        return validate_postcode_and_return_country(postcode, form=self)

    def search(self):
        return self.perform_search(
            self,
            self.cleaned_data.get("postcode"),
            self.cleaned_data.get("categories"),
            self.cleaned_data.get("page", 1),
        )


class SingleCategorySearchForm(AdviserRootForm, BaseSearch):
    page = forms.IntegerField(required=False, widget=forms.HiddenInput())

    def __init__(self, categories=None, *args, **kwargs):
        kwargs.setdefault("label_suffix", "")
        super(AdviserRootForm, self).__init__(*args, **kwargs)
        self.categories = categories if categories is not None else []

    def clean(self):
        data = self.cleaned_data
        postcode = data.get("postcode")
        categories = self.data.get("categories")

        if not postcode:
            self.add_error("postcode", _("Enter a postcode"))
            return data

        if postcode:
            valid_postcode = self.validate_postcode_and_return_country(postcode)
            if not valid_postcode:
                self.add_error("postcode", _("Enter a valid postcode"))
            else:
                self._country_from_valid_postcode = valid_postcode

        # Check if categories are provided
        if not categories:
            self.add_error("categories", _("Category is required."))
        else:
            self.categories = [categories]

        return data

    @property
    def current_page(self):
        return self.cleaned_data.get("page", 1)

    def validate_postcode_and_return_country(self, postcode):
        return validate_postcode_and_return_country(postcode, form=self)

    def search(self):
        return self.perform_search(
            self,
            self.cleaned_data.get("postcode"),
            self.categories,
            self.cleaned_data.get("page", 1),
        )
