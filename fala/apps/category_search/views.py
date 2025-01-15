# coding=utf-8
from django.conf import settings
from django.urls import reverse
from django.views.generic import TemplateView
from django.http import HttpResponse
from category_search.forms import SingleCategorySearchForm
from django.shortcuts import redirect
from fala.common.mixin_for_views import CommonContextMixin, CategoryMixin
from fala.common.category_messages import CATEGORY_MESSAGES


class SingleCategorySearchView(CommonContextMixin, CategoryMixin, TemplateView):
    template_name = "adviser/single_category_search.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if not settings.FEATURE_FLAG_SINGLE_CATEGORY_SEARCH_FORM:
            return redirect("adviser")

        result = self.setup_category(request, *args, **kwargs)
        if isinstance(result, HttpResponse):
            return result

        self.category_code = result

        category_message = CATEGORY_MESSAGES.get(self.category_slug, "")
        category_display_name = self.category_slug.replace("-", " ").title()

        form = SingleCategorySearchForm(initial={"categories": [self.category_code]}, data=request.GET or None)

        search_url = reverse("results")

        context.update(
            {
                "form": form,
                "data": {},
                "errorList": [],
                "category_slug": self.category_slug,
                "category_code": self.category_code,
                "category_display_name": category_display_name,
                "category_message": category_message,
                "search_url": search_url,
            }
        )
        return self.render_to_response(context)
