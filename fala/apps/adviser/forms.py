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
    def clean(self):
        cleaned_data = super(AdviserSearchForm, self).clean()
        if cleaned_data.get('search_type') == 'location' and not \
                cleaned_data.get('postcode'):
            raise forms.ValidationError(
                _('Please enter a postcode')
            )
        elif cleaned_data.get('search_type') == 'organisation' and not \
                cleaned_data.get('organisation_name'):
            raise forms.ValidationError(
                _('Please enter an organisation')
            )
        return cleaned_data

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
