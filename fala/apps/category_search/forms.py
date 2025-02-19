# coding=utf-8
from django import forms
from django.utils.translation import gettext_lazy as _
from fala.common.utils import validate_postcode_and_return_country
from fala.common.base_form_components import AdviserRootForm, BaseSearch


class CategorySearchForm(AdviserRootForm, BaseSearch):
    page = forms.IntegerField(required=False, widget=forms.HiddenInput())

    def __init__(self, categories=None, *args, **kwargs):
        kwargs.setdefault("label_suffix", "")
        super(AdviserRootForm, self).__init__(*args, **kwargs)
        self.categories = categories if categories is not None else []

    def clean(self):
        data = self.cleaned_data
        postcode = data.get("postcode")
        self.categories = data.get("categories", [])

        # this skips form validation if no postcode is in the request (e.g. during redirects)
        if "postcode" not in self.data:
            return data

        if postcode:
            valid_postcode = self.validate_postcode_and_return_country(postcode)
            if not valid_postcode:
                self.add_error("postcode", _("Enter a valid postcode"))
            else:
                self._country_from_valid_postcode = valid_postcode
        else:
            self.add_error("postcode", _("Enter a postcode"))
            return data

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
