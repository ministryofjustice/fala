# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import gettext_lazy as _

from laalaa.api import PROVIDER_CATEGORY_CHOICES


SEARCH_TYPE_CHOICES = [
    ('location', _('Location')),
    ('organisation', _('Organisation')),
]

ORGANISATION_TYPES = [
    'Charity or Voluntary Org',
    'Mediation Service',
    'Private Company',
    'Solicitor',
]

ORGANISATION_TYPES_CHOICES = tuple(zip(ORGANISATION_TYPES,
                                       ORGANISATION_TYPES))


class AdviserSearchForm(forms.Form):
    search_type = forms.ChoiceField(
        choices=SEARCH_TYPE_CHOICES,
        widget=forms.RadioSelect(),
        initial=SEARCH_TYPE_CHOICES[0][0])
    postcode = forms.CharField(
        label=_('Postcode'),
        max_length=10,
        help_text=_('Enter a postcode, town or city'),
        required=False)
    organisation_name = forms.CharField(
        label=_('Organisation'),
        max_length=100,
        required=False)
    organisation_types = forms.MultipleChoiceField(
        choices=ORGANISATION_TYPES_CHOICES,
        widget=forms.CheckboxSelectMultiple(),
        required=False)
    category = forms.NullBooleanField(
        label=_('Category'),
        widget=forms.CheckboxInput()
    )
    categories = forms.MultipleChoiceField(
        choices=PROVIDER_CATEGORY_CHOICES,
        widget=forms.CheckboxSelectMultiple(),
        required=False)
