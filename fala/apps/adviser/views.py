# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from django.utils.translation import gettext as _

from laalaa import api as laalaa

from .forms import AdviserSearchForm, SEARCH_TYPE_CHOICES


class IndexView(TemplateView):
    template_name = 'adviser/index.html'

    def get(self, request, *args, **kwargs):
        form = AdviserSearchForm(data=request.GET or None)

        try:
            data = laalaa.find(
                postcode=request.GET.get('postcode'),
                categories=request.GET.getlist('categories'),
                page=request.GET.get('page'),
                organisation_types=request.GET.getlist('organisation_types'),
                organisation_name=request.GET.getlist('organisation_name'),
            )
            if 'error' in data:
                raise Exception(data['error'])
        except laalaa.LaaLaaError:
            raise Exception(u"%s %s" % (
                _('Error looking up legal advisers.'),
                _('Please try again later.')
            ))

        context = self.get_context_data(**kwargs)
        context.update({
            'data': data,
            'form': form,
            'categories': [{'id': c[0], 'name': c[1]} for c in laalaa.PROVIDER_CATEGORIES.items()],
        })

        return self.render_to_response(context)


