# coding=utf-8
from django.urls import reverse
from django.views.generic import ListView
from fala.apps.adviser.forms import AdviserSearchForm
from fala.apps.category_search.forms import CategorySearchForm
from fala.common.states import EnglandOrWalesState, OtherJurisdictionState, ErrorState, CategorySearchErrorState
from fala.common.mixin_for_views import CommonContextMixin, CategoryMixin, TranslationMixin
from fala.common.category_messages import CATEGORY_MESSAGES
from fala.common.regions import Region


class ResultsView(
    CommonContextMixin, TranslationMixin, CategoryMixin, ListView, EnglandOrWalesState, OtherJurisdictionState
):
    def get(self, request, *args, **kwargs):
        self.tailored_results = self.request.GET.get("tailored_results", False)
        categories = self.request.GET.getlist("categories", [])
        self.category_code = categories[0] if categories else ""
        self.sub_category_code = categories[1] if len(categories) > 1 else ""
        self.category_code = self.request.GET.get("categories", False)
        self.translation_link = self.translation_link(request)
        self.language = self.language(request)

        if self.tailored_results:
            form_class = CategorySearchForm
        else:
            form_class = AdviserSearchForm

        form = form_class(data=request.GET or None)

        if form.is_valid():
            region = form.region
            if region == Region.ENGLAND_OR_WALES or region == Region.SCOTLAND:
                self.state = EnglandOrWalesState(request, form)
            else:
                self.state = OtherJurisdictionState(region, form.cleaned_data["postcode"])
        else:
            if self.tailored_results:
                # using CategoryMixin to access category_display_name & category_message, so we show this on CategorySearchErrorState view
                self.setup_category(request, *args, **kwargs)
                category_display_name = (self.category_slug or "").replace("-", " ").title()
                category_message = CATEGORY_MESSAGES.get(self.category_slug, "")
                categories = self.request.GET.getlist("categories", [])

                # this is so we can use category_code, sub_category_code & search_url, when conducting a search from CategorySearchErrorState view
                category_code = categories[0] if categories else ""
                sub_category_code = categories[1] if len(categories) > 1 else ""

                # this is so that we can get correct hlpas display name onto CategorySearchErrorState view
                category_slug = categories[0] if categories else ""

                search_url = reverse("results")

                self.state = CategorySearchErrorState(
                    form,
                    category_display_name,
                    category_message,
                    category_code,
                    sub_category_code,
                    search_url,
                    category_slug,
                )
            else:
                self.state = ErrorState(form)

        return super().get(self, request, *args, **kwargs)

    def get_template_names(self):
        return ["adviser/" + self.state.template_name]

    def get_queryset(self):
        return self.state.get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tailored_results"] = self.tailored_results
        context["category_code"] = self.category_code
        context["sub_category_code"] = self.sub_category_code
        context.update({"translation_link": self.translation_link, "language": self.language})
        context.update(self.state.get_context_data())
        return context
