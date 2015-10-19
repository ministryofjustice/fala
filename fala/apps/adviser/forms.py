# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import gettext_lazy as _

import laalaa.api as laalaa


SEARCH_TYPE_CHOICES = [
    ('location', _('Location')),
    ('organisation', _('Organisation')),
]

ORGANISATION_TYPES_CHOICES = [
    ('Charity or Voluntary Org', 'Charity or Voluntary Organisations'),
    ('Mediation', 'Mediation Service'),
    ('Private Company', 'Private Company'),
    ('Solicitor', 'Solicitor'),
]


class FalaTextInput(forms.TextInput):
    def __init__(self, attrs={}):
        class_attr = ' '.join([c for c in ['form-control', attrs.get('class')] if c])
        attrs.update({'class': class_attr})

        super(FalaTextInput, self).__init__(attrs)


class AdviserSearchForm(forms.Form):

    page = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput()
    )

    postcode = forms.CharField(
        label=_('Enter postcode'),
        max_length=10,
        help_text=_('Enter a postcode, town or city'),
        required=False,
        widget=FalaTextInput(attrs={
            'placeholder': _('e.g. SW1H 9AJ')
        }))

    organisation_name = forms.CharField(
        label=_('Organisation name'),
        max_length=100,
        required=False,
        widget=FalaTextInput(attrs={
            'placeholder': _('e.g. Winthorpes')
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

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(AdviserSearchForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(AdviserSearchForm, self).clean()
        return cleaned_data

    def search(self):
        if self.is_valid():
            try:
                data = laalaa.find(
                    postcode=self.cleaned_data.get('postcode'),
                    categories=self.cleaned_data.get('categories'),
                    page=self.cleaned_data.get('page', 1),
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
