# coding=utf-8
from django import forms
from django.utils.translation import gettext_lazy as _

import laalaa.api as laalaa
import re

SEARCH_TYPE_CHOICES = [("location", _("Location")), ("organisation", _("Organisation"))]

ORGANISATION_TYPES_CHOICES = [
    ("Charity or Voluntary Org", "Charity or Voluntary Organisations"),
    ("Mediation", "Mediation Service"),
    ("Private Company", "Private Company"),
    ("Solicitor", "Solicitor"),
]


class FalaTextInput(forms.TextInput):
    def __init__(self, attrs={}):
        class_attr = " ".join([c for c in ["form-control", attrs.get("class")] if c])
        attrs.update({"class": class_attr})

        super(FalaTextInput, self).__init__(attrs)


class AdviserSearchForm(forms.Form):

    page = forms.IntegerField(required=False, widget=forms.HiddenInput())

    postcode = forms.CharField(
        label=_("Enter postcode, town or city"),
        max_length=30,
        help_text=_("For example, <span class='notranslate'>SW1H 9AJ</span>"),
        required=False,
        widget=FalaTextInput(attrs={"class": "govuk-input govuk-!-width-one-third"}),
    )

    name = forms.CharField(
        label=_("Organisation name"),
        max_length=100,
        required=False,
        widget=FalaTextInput(attrs={"class": "govuk-input govuk-!-width-one-third"}),
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

    def clean(self):
        data = self.cleaned_data
        if not data.get("postcode") and not data.get("name"):
            raise forms.ValidationError(_("Enter a postcode or an organisation name"))
        else:
            msg1 = "This service does not cover "
            msg2 = "Try a postcode, town or city in England or Wales."
            x = "England or Wales. "
            if re.search("[Bb][Tt][0-9]", data.get("postcode")):
                x = "Northern Ireland. "
            elif re.search("[Ii][Mm][0-9]", data.get("postcode")):
                x = "the Isle of Man. "
            elif re.search("[Jj][Ee][0-9]", data.get("postcode")):
                x = "Jersey. "
            elif re.search("[Gg][Yy][1][0]", data.get("postcode")):
                x = "Sark or Guernsey. "
            elif re.search("[Gg][Yy][9]", data.get("postcode")):
                x = "Alderney or Guernsey. "
            elif re.search("[Gg][Yy][0-8]", data.get("postcode")):
                x = "Guernsey. "
            if x != "England or Wales. ":
                self.add_error("postcode", u"%s %s %s" % (_(msg1), _(x), _(msg2)))
        return data

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
                    "postcode", u"%s %s" % (_("Error looking up legal advisers."), _("Please try again later."))
                )
        return {}
