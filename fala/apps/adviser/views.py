# -*- coding: utf-8 -*-
from django.conf import settings
from django.views.generic import TemplateView

from .forms import AdviserSearchForm


class IndexView(TemplateView):
    template_name = 'adviser/index.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = AdviserSearchForm(data=request.GET or None)

        context.update({
            'form': form,
            'data': form.search(),
            'LAALAA_API_HOST': settings.LAALAA_API_HOST,
        })

        return self.render_to_response(context)


