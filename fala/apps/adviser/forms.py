# coding=utf-8

from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.conf import settings

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


class AdviserSearchForm(forms.Form):
    # Only used with FEATURE_FLAG_NO_MAP False
    REGION_NAMES = {
        Region.NI: "Northern Ireland. ",
        Region.IOM: "the Isle of Man. ",
        Region.JERSEY: "Jersey. ",
        Region.GUERNSEY: "Guernsey. ",
        Region.SCOTLAND: "Scotland. ",
    }

    page = forms.IntegerField(required=False, widget=forms.HiddenInput())

    postcode = CapitalisedPostcodeField(
        label=_("Postcode"),
        max_length=30,
        help_text=_(
            mark_safe("For example, <span class='notranslate' translate='no' id='postcode-description'>" "SW1H</span>")
        ),
        required=False,
        widget=FalaTextInput(),
    )

    name = forms.CharField(
        label=_("Organisation name"),
        max_length=100,
        required=False,
        widget=FalaTextInput(),
    )

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
        if not settings.FEATURE_FLAG_NO_MAP:
            self.fields["postcode"].label = _("Enter postcode")
            self.fields["postcode"].help_text = _(
                "For example, <span class='notranslate' translate='no' id='postcode-description'>SW1H 9AJ</span>"
            )

    def clean(self):
        data = self.cleaned_data
        postcode = data.get("postcode")
        if not postcode and not data.get("name"):
            raise forms.ValidationError(_("Enter a postcode or an organisation name"))
        else:
            if settings.FEATURE_FLAG_NO_MAP:
                if postcode and self.region == Region.ENGLAND_OR_WALES and not self._valid_postcode(postcode):
                    self.add_error("postcode", (_("Enter a valid postcode")))
            else:
                region = self.region
                if region != Region.ENGLAND_OR_WALES:
                    region_error = self.REGION_NAMES[region]
                    msg1 = "This service does not cover "
                    msg2 = "Try a postcode, town or city in England or Wales."
                    self.add_error("postcode", "%s %s" % (_(" ".join((msg1, region_error))), _(msg2)))
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
