# coding=utf-8
from django.urls import reverse
from django.views.generic import ListView
from fala.apps.adviser.forms import AdviserSearchForm, SingleCategorySearchForm
from fala.common.states import EnglandOrWalesState, OtherJurisdictionState, ErrorState, SingleSearchErrorState
from fala.common.mixin_for_views import CommonContextMixin, CategoryMixin
from fala.common.category_messages import CATEGORY_MESSAGES
from fala.common.regions import Region


class ResultsView(CommonContextMixin, CategoryMixin, ListView, EnglandOrWalesState, OtherJurisdictionState):
    def get(self, request, *args, **kwargs):
        self.tailored_results = self.request.GET.get("tailored_results", False)

        if self.tailored_results:
            form_class = SingleCategorySearchForm
        else:
            form_class = AdviserSearchForm

        form = form_class(data=request.GET or None)

        if form.is_valid():
            region = form.region
            if region == Region.ENGLAND_OR_WALES or region == Region.SCOTLAND:
                self.state = EnglandOrWalesState(form)
            else:
                self.state = OtherJurisdictionState(region, form.cleaned_data["postcode"])
        else:
            if self.tailored_results:
                # using CategoryMixin to access category_display_name & category_message, so we show this on SingleSearchErrorState view
                self.setup_category(request, *args, **kwargs)
                category_display_name = self.category_slug.replace("-", " ").title()
                category_message = CATEGORY_MESSAGES.get(self.category_slug, "")

                # this is so we can use category_code & search_url, when conducting a search from SingleSearchErrorState view
                category_code = self.request.GET.get("categories", "")
                search_url = reverse("results")

                # this is so that we can get correct hlpas display name onto SingleSearchErrorState view
                category_slug = self.request.GET.get("categories")

                self.state = SingleSearchErrorState(
                    form, category_display_name, category_message, category_code, search_url, category_slug
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
        context.update(self.state.get_context_data())
        return context
