# coding=utf-8
from django.conf import settings
from django.urls import resolve, reverse
from django.views.generic import TemplateView, ListView
from django.http import HttpResponse
import os
from django.views import View
from .forms import AdviserSearchForm, AdviserRootForm
from .regions import Region
from django.shortcuts import redirect, render
from .models import EnglandOrWalesState, ErrorState, OtherJurisdictionState
from .forms import SingleCategorySearchForm
from .utils import CATEGORY_MESSAGES, CATEGORY_DISPLAY_NAMES, get_category_display_name, get_category_code_from_slug
import logging


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


logger = logging.getLogger(__name__)


class SingleCategorySearchView(TemplateView):
    template_name = "adviser/single_category_search.html"

    def get(self, request, *args, **kwargs):
        category_code = request.GET.get("categories")

        if category_code:
            category_slug = get_category_display_name(category_code)
            if category_slug:
                return redirect("single_category_search", category=category_slug)
            else:
                return redirect("search")

        category_slug = kwargs.get("category")
        if not category_slug:
            return redirect("search")

        if not category_code or category_code == "None":
            category_code = get_category_code_from_slug(category_slug)

        category_message = CATEGORY_MESSAGES.get(category_slug, "")
        category_display_name = CATEGORY_DISPLAY_NAMES.get(category_slug, category_slug.replace("-", " ").title())

        form = SingleCategorySearchForm(categories=category_slug, data=request.GET or None)

        # Determine the state and results
        if form.is_valid():
            logger.debug("Form is valid. Determining region.")
            region = form.region  # Now `region` will be correctly determined
            if region in [Region.ENGLAND_OR_WALES, Region.SCOTLAND]:
                logger.debug("Region is England or Wales or Scotland.")
                state = EnglandOrWalesState(form)
            else:
                logger.warning("Region is outside of England or Wales. Using OtherJurisdictionState.")
                state = OtherJurisdictionState(region, form.cleaned_data["postcode"])
        else:
            logger.error("Form is invalid: %s", form.errors)
            state = ErrorState(form)

        # Let the state handle the logic for results
        results = state.get_queryset()
        template_name = state.template_name

        search_url = reverse("single_category_search", kwargs={"category": category_slug})

        context = {
            "form": form,
            "category_slug": category_slug,
            "category_code": category_code,
            "category_display_name": category_display_name,
            "category_message": category_message,
            "results": results,
            "data": results,
            "search_url": search_url,
        }

        return render(request, self.template_name, context)
        # so to show the search page this must be self.template_name
        # but when i want to show results it needs to be template_name
        # so that it can take it from EnglandOrWalesState which uses results.html

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_url"] = reverse("single_category_search", kwargs={"category": kwargs.get("category_slug")})
        return context


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


class SearchView(CommonContextMixin, ListView, EnglandOrWalesState, OtherJurisdictionState):
    def get(self, request, *args, **kwargs):
        form = AdviserSearchForm(data=request.GET or None)

        if form.is_valid():
            region = form.region
            if region == Region.ENGLAND_OR_WALES or region == Region.SCOTLAND:
                self.state = EnglandOrWalesState(form)
            else:
                self.state = OtherJurisdictionState(region, form.cleaned_data["postcode"])
        else:
            self.state = ErrorState(form)

        return super().get(self, request, *args, **kwargs)

    def get_template_names(self):
        return ["adviser/" + self.state.template_name]

    def get_queryset(self):
        return self.state.get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(self.state.get_context_data())
        return context
