# coding=utf-8
from django.conf import settings
from django.shortcuts import redirect
from fala.common.category_manager import CategoryManager
from django.utils import translation


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


class TranslationMixin:
    def translation_link(self, request):
        user_language = request.COOKIES.get("django_language", "en")
        translation.activate(user_language)
        if user_language == "cy":
            return f"<a class='govuk-body govuk-link' id='language_switcher_link' href='/set_language?language_code=en&return_link={request.get_full_path()}'>English</a> / Cymraeg"
        else:
            return f"English / <a class='govuk-body govuk-link' id='language_switcher_link' href='/set_language?language_code=cy&return_link={request.get_full_path()}'>Cymraeg</a>"


class CategoryMixin:
    def setup_category(self, request, **kwargs):
        category_code = request.GET.get("categories")

        if not category_code:
            self.category_slug = kwargs.get("category")
            if not self.category_slug:  # Redirect if no category specified
                return redirect("adviser")
            # if there is a slug, then retrieve the code based on the slug.
            category_code = CategoryManager.category_code_from(self.category_slug)
            if not category_code:
                return redirect("adviser")
        else:
            self.category_slug = CategoryManager.slug_from(category_code)
            if self.category_slug:
                return redirect("category_search", category=self.category_slug)
            else:
                return redirect("adviser")
        return category_code
