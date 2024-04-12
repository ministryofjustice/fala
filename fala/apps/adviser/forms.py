# coding=utf-8
from enum import Enum

from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _

import fala.apps.laalaa.api as laalaa
import re

SEARCH_TYPE_CHOICES = [("location", _("Location")), ("organisation", _("Organisation"))]

ORGANISATION_TYPES_CHOICES = [
    ("Charity or Voluntary Org", "Charity or Voluntary Organisations"),
    ("Mediation", "Mediation Service"),
    ("Private Company", "Private Company"),
    ("Solicitor", "Solicitor"),
]

Region = Enum(
    "Region",
    [
        "NI",
        "IOM",
        "JERSEY",
        "GUERNSEY",
        "ENGLAND_OR_WALES",
        "SCOTLAND",
    ],
)

REGION_ERRORS = {
    Region.NI: "Northern Ireland. ",
    Region.IOM: "the Isle of Man. ",
    Region.JERSEY: "Jersey. ",
    Region.GUERNSEY: "Guernsey. ",
    Region.SCOTLAND: "Scotland. ",
}

SCOTTISH_PREFIXES = [
    "AB","DD","DG","EH","FK","G1","G2","G3","G4","G5","G6","G7","G8","G9","G0","HS","IV","KA","KW","KY","ML","PA","PH","TD","ZE"
]

class FalaTextInput(forms.TextInput):
    def __init__(self, attrs={}):
        class_attr = " ".join([c for c in ["govuk-input govuk-!-width-one-third", attrs.get("class")] if c])
        attrs.update({"class": class_attr})

        super(FalaTextInput, self).__init__(attrs)

class RegionNotFoundException(Exception):
    def __init__(self, region):
        self.region = region
        super(RegionNotFoundException, self).__init__()

class AdviserSearchForm(forms.Form):
    page = forms.IntegerField(required=False, widget=forms.HiddenInput())

    postcode = forms.CharField(
        label=_("Enter postcode"),
        max_length=30,
        help_text=_("For example, <span class='notranslate' translate='no'>SW1H 9AJ</span>"),
        required=False,
        widget=FalaTextInput(),
    )

    name = forms.CharField(label=_("Organisation name"), max_length=100, required=False, widget=FalaTextInput())

    type = forms.MultipleChoiceField(
        label=_("Organisation type"),
        choices=ORGANISATION_TYPES_CHOICES,
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    categories = forms.MultipleChoiceField(
        label=_("Category"),
        choices=laalaa.PROVIDER_CATEGORY_CHOICES,
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("label_suffix", "")
        super(AdviserSearchForm, self).__init__(*args, **kwargs)

    def clean(self):
        data = self.cleaned_data
        if not data.get("postcode") and not data.get("name"):
            raise forms.ValidationError(_("Enter a postcode or an organisation name"))
        else:
            if not settings.FEATURE_FLAG_NO_MAP:
                region = self._region()
                if region != Region.ENGLAND_OR_WALES:
                    region_error = REGION_ERRORS[region]
                    msg1 = "This service does not cover "
                    msg2 = "Try a postcode, town or city in England or Wales."
                    self.add_error("postcode", "%s %s" % (_(" ".join((msg1, region_error))), _(msg2)))
        return data

    def _region(self):
        postcodeNoSpace = self.cleaned_data.get("postcode").replace(" ", "")
        if re.search(r"^BT[0-9]", postcodeNoSpace, flags=re.IGNORECASE):
            return Region.NI
        elif re.search(r"^IM[0-9]", postcodeNoSpace, flags=re.IGNORECASE):
            return Region.IOM
        elif re.search(r"^JE[0-9]", postcodeNoSpace, flags=re.IGNORECASE):
            return Region.JERSEY
        elif re.search(r"^GY[1][0]", postcodeNoSpace, flags=re.IGNORECASE):
            return Region.GUERNSEY
        elif re.search(r"^GY[9]", postcodeNoSpace, flags=re.IGNORECASE):
            return Region.GUERNSEY
        elif re.search(r"^GY[0-8]", postcodeNoSpace, flags=re.IGNORECASE):
            return Region.GUERNSEY
        elif postcodeNoSpace[:2] in SCOTTISH_PREFIXES:
            return Region.SCOTLAND
        else:
            return Region.ENGLAND_OR_WALES

    @property
    def current_page(self):
        return self.cleaned_data.get("page", 1)

    def search(self):
        if self.is_valid():
            try:
                if settings.FEATURE_FLAG_NO_MAP:
                    region = self._region()
                    if region != Region.ENGLAND_OR_WALES:
                        raise RegionNotFoundException(region)
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
