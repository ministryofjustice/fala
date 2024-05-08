# coding=utf-8
from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.conf import settings

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
        class_attr = " ".join([c for c in ["govuk-input govuk-!-width-one-third", attrs.get("class")] if c])
        attrs.update({"class": class_attr})

        super(FalaTextInput, self).__init__(attrs)


class AdviserSearchForm(forms.Form):
    page = forms.IntegerField(required=False, widget=forms.HiddenInput())

    postcode = forms.CharField(
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
                "For example, <span class='notranslate' translate='no'>SW1H 9AJ</span>"
            )

    def clean(self):
        data = self.cleaned_data
        if not data.get("postcode") and not data.get("name"):
            raise forms.ValidationError(_("Enter a postcode or an organisation name"))
        else:
            postcodeNoSpace = data.get("postcode").replace(" ", "")
            msg1 = "This service does not cover "
            msg2 = "Try a postcode, town or city in England or Wales."
            region = "England or Wales. "
            if re.search(r"^BT[0-9]", postcodeNoSpace, flags=re.IGNORECASE):
                region = "Northern Ireland. "
            elif re.search(r"^IM[0-9]", postcodeNoSpace, flags=re.IGNORECASE):
                region = "the Isle of Man. "
            elif re.search(r"^JE[0-9]", postcodeNoSpace, flags=re.IGNORECASE):
                region = "Jersey. "
            elif re.search(r"^GY[1][0]", postcodeNoSpace, flags=re.IGNORECASE):
                region = "Sark or Guernsey. "
            elif re.search(r"^GY[9]", postcodeNoSpace, flags=re.IGNORECASE):
                region = "Alderney or Guernsey. "
            elif re.search(r"^GY[0-8]", postcodeNoSpace, flags=re.IGNORECASE):
                region = "Guernsey. "
            if region != "England or Wales. ":
                self.add_error("postcode", "%s %s" % (_(" ".join((msg1, region))), _(msg2)))
        return data

    @property
    def current_page(self):
        return self.cleaned_data.get("page", 1)

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
