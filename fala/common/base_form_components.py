# coding=utf-8
from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from fala.common.regions import Region
import fala.apps.laalaa.api as laalaa


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
