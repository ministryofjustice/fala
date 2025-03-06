from django.utils.translation import gettext_lazy as _


class CategoryManager:
    """Manages category mappings and lookups."""

    CATEGORY_CODE_TO_SLUG = {
        "aap": "claims-against-public-authorities",
        "med": "clinical-negligence",
        "com": "community-care",
        "crm": "crime",
        "deb": "debt",
        "disc": "discrimination",
        "edu": "education",
        "mat": "family",
        "fmed": "family-mediation",
        "hou": "housing",
        "hlpas": "housing-loss-prevention-advice-service",
        "immas": "immigration-or-asylum",
        "mhe": "mental-health",
        "mosl": "modern-slavery",
        "pl": "prison-law",
        "pub": "public-law",
        "wb": "welfare-benefits",
    }

    # These are required for django translations, so that the Welsh
    # category translations are not deleted when running makemessages.
    CATEGORIES_FOR_TRANSLATION = [
        _("Claims Against Public Authorities"),
        _("Clinical negligence"),
        _("Community care"),
        _("Crime"),
        _("Debt"),
        _("Discrimination"),
        _("Education"),
        _("Family"),
        _("Family mediation"),
        _("Housing"),
        _("Housing Loss Prevention Advice Service"),
        _("Immigration or asylum"),
        _("Mental health"),
        _("Modern slavery"),
        _("Prison law"),
        _("Public law"),
        _("Welfare benefits"),
    ]

    SLUG_TO_CATEGORY_CODE = {slug: category_code for category_code, slug in CATEGORY_CODE_TO_SLUG.items()}

    @classmethod
    def category_code_from(cls, slug):
        return CategoryManager.SLUG_TO_CATEGORY_CODE.get(slug, None)

    @classmethod
    def slug_from(cls, category_code):
        return CategoryManager.CATEGORY_CODE_TO_SLUG.get(category_code, None)
