# coding=utf-8
from django.conf import settings
from django.urls import resolve, reverse
from django.views.generic import TemplateView, ListView, View
from django.http import HttpResponse
import os
from .forms import AdviserSearchForm, AdviserRootForm, SingleCategorySearchForm
from fala.apps.adviser.regions import Region
from django.shortcuts import redirect
from fala.common.states import EnglandOrWalesState, OtherJurisdictionState, ErrorState, SingleSearchErrorState
from fala.apps.constants.category_manager import CategoryManager
from fala.apps.constants.category_messages import CATEGORY_MESSAGES


class RobotsTxtView(View):
    def get(self, request):
        environment = os.getenv("ENVIRONMENT", "development").lower()

        if environment == "production":
            content = "User-agent: *\nDisallow:\n"  # Allow all
        else:
            content = "User-agent: *\nDisallow: /\n"  # Disallow all for staging/UAT

        return HttpResponse(content, content_type="text/plain")


class SecurityTxtView(View):
    def get(self, request):
        file_path = os.path.join(settings.BASE_DIR, "fala", "public", "security.txt")
        try:
            with open(file_path, "r") as f:
                content = f.read()
            return HttpResponse(content, content_type="text/plain")
        except FileNotFoundError:
            return HttpResponse("security.txt not found.", content_type="text/plain", status=404)


class CommonContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            {
                # this is so that `govuk_frontend_jinja/template.html` can be extended and without CSP complaining
                "cspNonce": getattr(self.request, "csp_nonce", None),
                # this is added in so that an additional class is added the <body>
                "bodyClasses": f"fala-{settings.ENVIRONMENT}",
                "FEATURE_FLAG_MAINTENANCE_MODE": settings.FEATURE_FLAG_MAINTENANCE_MODE,
            }
        )
        return context


class CategoryMixin:
    def setup_category(self, request, *args, **kwargs):
        category_code = request.GET.get("categories")

        if not category_code:
            self.category_slug = kwargs.get("category")
            if not self.category_slug:  # Redirect if no category specified
                return redirect("search")
            # if there is a slug, then retrieve the code based on the slug.
            category_code = CategoryManager.category_code_from(self.category_slug)
            if not category_code:
                return redirect("search")
        else:
            self.category_slug = CategoryManager.slug_from(category_code)
            if self.category_slug:
                return redirect("single_category_search", category=self.category_slug)
            else:
                return redirect("search")
        return category_code


class SingleCategorySearchView(CommonContextMixin, CategoryMixin, TemplateView):
    template_name = "adviser/single_category_search.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if not settings.FEATURE_FLAG_SINGLE_CATEGORY_SEARCH_FORM:
            return redirect("search")

        result = self.setup_category(request, *args, **kwargs)
        if isinstance(result, HttpResponse):
            return result

        self.category_code = result

        category_message = CATEGORY_MESSAGES.get(self.category_slug, "")
        category_display_name = self.category_slug.replace("-", " ").title()

        form = SingleCategorySearchForm(initial={"categories": [self.category_code]}, data=request.GET or None)

        search_url = reverse("search")

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


class AdviserView(CommonContextMixin, TemplateView):
    template_name = "adviser/search.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = AdviserRootForm(data=request.GET or None)
        view_name = resolve(request.path_info).url_name
        current_url = reverse(view_name)

        context.update(
            {
                "form": form,
                "data": {},
                "errorList": [],
                "current_url": current_url,
                "CHECK_LEGAL_AID_URL": settings.CHECK_LEGAL_AID_URL,
            }
        )

        return self.render_to_response(context)


class AccessibilityView(CommonContextMixin, TemplateView):
    template_name = "adviser/accessibility_statement.html"


class PrivacyView(CommonContextMixin, TemplateView):
    template_name = "adviser/privacy.html"


class CookiesView(CommonContextMixin, TemplateView):
    template_name = "adviser/cookies.html"


class SearchView(CommonContextMixin, CategoryMixin, ListView, EnglandOrWalesState, OtherJurisdictionState):
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
                search_url = reverse("search")

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
