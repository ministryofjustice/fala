# coding=utf-8
from django.conf import settings
from django.urls import resolve, reverse
from django.views.generic import TemplateView

from .forms import AdviserSearchForm


class AdviserView(TemplateView):
    # https://docs.djangoproject.com/en/5.0/topics/class-based-views/#usage-in-your-urlconf - this is how `template_name`
    if settings.FEATURE_FLAG_NO_MAP:
        template_name = "adviser/search.html"
    else:
        template_name = "adviser/search_old.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = AdviserSearchForm(data=request.GET or None)
        view_name = resolve(request.path_info).url_name
        current_url = reverse(view_name)

        context.update(
            {
                "form": form,
                "data": form.search(),
                "current_url": current_url,
                "GOOGLE_MAPS_API_KEY": settings.GOOGLE_MAPS_API_KEY,
                "LAALAA_API_HOST": settings.LAALAA_API_HOST,
                "FEATURE_FLAG_NO_MAP": settings.FEATURE_FLAG_NO_MAP,
                "CHECK_LEGAL_AID_URL": settings.CHECK_LEGAL_AID_URL,
            }
        )

        return self.render_to_response(context)


class AccessibilityView(TemplateView):
    template_name = "adviser/accessibility-statement.html"
