# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import gettext_lazy as _

import laalaa.api as laalaa


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


class FalaTextInput(forms.TextInput):
    def __init__(self, attrs={}):
        class_attr = ' '.join([c for c in ['form-control', attrs.get('class')] if c])
        attrs.update({'class': class_attr})

        super(FalaTextInput, self).__init__(attrs)


class AdviserSearchForm(forms.Form):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(AdviserSearchForm, self).__init__(*args, **kwargs)

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

    def search(self):
        if self.is_valid():
            try:
                data = laalaa.find(
                    postcode=self.cleaned_data.get('postcode'),
                    categories=self.cleaned_data.get('categories'),
                    page=self.cleaned_data.get('page'),
                    organisation_types=self.cleaned_data.get('organisation_types'),
                    organisation_name=self.cleaned_data.get('organisation_name'),
                )
                if 'error' in data:
                    self.add_error('postcode', (data['error']))
                    return {}
                return data
            except laalaa.LaaLaaError:
                self.add_error('postcode', u"%s %s" % (
                    _('Error looking up legal advisers.'),
                    _('Please try again later.')
                ))
        return {}


class AdviserSearchByLocationForm(AdviserSearchForm):

    postcode = forms.CharField(
        label=_('Enter postcode'),
        max_length=10,
        help_text=_('Enter a postcode, town or city'),
        required=True,
        widget=FalaTextInput(attrs={
            'placeholder': _('e.g. SW1H 9AJ'),
            'autofocus': True
        }))

    organisation_types = forms.MultipleChoiceField(
        label=_('Organisation type'),
        choices=ORGANISATION_TYPES_CHOICES,
        widget=forms.CheckboxSelectMultiple(),
        required=False)

    categories = forms.MultipleChoiceField(
        label=_('Category'),
        choices=laalaa.PROVIDER_CATEGORY_CHOICES,
        widget=forms.CheckboxSelectMultiple(),
        required=False)


class AdviserSearchByOrganisationForm(AdviserSearchForm):

    organisation_name = forms.CharField(
        label=_('Organisation name'),
        max_length=100,
        required=True,
        widget=FalaTextInput(attrs={
            'placeholder': _('e.g. Winthorpes'),
            'autofocus': True
        }))
