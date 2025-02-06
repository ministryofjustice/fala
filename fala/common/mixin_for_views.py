# coding=utf-8
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from fala.common.category_manager import CategoryManager


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
                "FEATURE_FLAG_WELSH_TRANSLATION": settings.FEATURE_FLAG_WELSH_TRANSLATION,
            }
        )
        return context

class CategoryMixin:
    def setup_category(self, request, *args, **kwargs):
        category_code = request.GET.get("categories", "")

        # Check if main category is in the URL (e.g., /check/family) i.e we have already redirected the user once
        main_category_from_url = kwargs.get("category")

        category_list = [c.strip() for c in category_code.split(",") if c.strip()]

        if main_category_from_url:
            main_category_code = CategoryManager.category_code_from(main_category_from_url)
            self.category_slug = main_category_from_url
        else:
            main_category_code = category_list[0] if category_list else None
            self.category_slug = CategoryManager.slug_from(main_category_code) if main_category_code else None

        main_category_code, secondary_category_code = (category_list + [None])[:2]

        # This prrevents a redirect loop that forces the user onto the search page for the secondary category
        if main_category_from_url == self.category_slug:
            return [main_category_code, secondary_category_code]

        redirect_url = reverse("category_search", kwargs={"category": self.category_slug})

        if secondary_category_code:
            redirect_url += f"?categories={secondary_category_code}"

        return redirect(redirect_url)

