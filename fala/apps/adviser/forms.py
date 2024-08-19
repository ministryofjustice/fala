# coding=utf-8

from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe

import laalaa.api as laalaa
import re

from .regions import Region, SCOTTISH_PREFIXES

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
# `def clean(self)` is the method triggering form validation, so have abstracted that into `AdviserSearchForm` form class
class AdviserRootForm(forms.Form):
    postcode = CapitalisedPostcodeField(
        label=_("Postcode"),
        max_length=30,
        help_text=_(mark_safe("For example, <span class='notranslate' translate='no'>SW1H</span>")),
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
        if not postcode and not data.get("name"):
            self.add_error("postcode", (_("Enter a postcode")))
            self.add_error("name", (_("Enter an organisation name")))
        else:
            if postcode and self.region == Region.ENGLAND_OR_WALES and not self._valid_postcode(postcode):
                self.add_error("postcode", (_("Enter a valid postcode")))

        return data

    @property
    def region(self):
        postcode_no_space = self.cleaned_data.get("postcode").replace(" ", "")
        if re.search(r"^BT[0-9]", postcode_no_space, flags=re.IGNORECASE):
            return Region.NI
        elif re.search(r"^IM[0-9]", postcode_no_space, flags=re.IGNORECASE):
            return Region.IOM
        elif re.search(r"^JE[0-9]", postcode_no_space, flags=re.IGNORECASE):
            return Region.JERSEY
        elif re.search(r"^GY[1][0]", postcode_no_space, flags=re.IGNORECASE):
            return Region.GUERNSEY
        elif re.search(r"^GY[9]", postcode_no_space, flags=re.IGNORECASE):
            return Region.GUERNSEY
        elif re.search(r"^GY[0-8]", postcode_no_space, flags=re.IGNORECASE):
            return Region.GUERNSEY
        elif postcode_no_space[:2] in SCOTTISH_PREFIXES:
            return Region.SCOTLAND
        else:
            return Region.ENGLAND_OR_WALES

    @property
    def current_page(self):
        return self.cleaned_data.get("page", 1)

    def _valid_postcode(self, postcode):
        try:
            data = laalaa.find(
                postcode=postcode,
                page=1,
            )
            return "error" not in data

        except laalaa.LaaLaaError:
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
