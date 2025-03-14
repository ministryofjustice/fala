# coding=utf-8
from django import forms
from django.utils.translation import gettext_lazy as _
from fala.common.regions import Region
from fala.common.utils import validate_postcode_and_return_country
from fala.common.base_form_components import AdviserRootForm, BaseSearch


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
