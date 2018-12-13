# coding=utf-8
from django import forms
from django.utils.translation import gettext_lazy as _


class FeedbackForm(forms.Form):
    referrer = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )
    feedback = forms.CharField(
        label=_('Please give us your feedback about this service'),
        max_length=10000,
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control m-full',
            'rows': 10
        }))
