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
        "immas": "immigration-asylum",
        "mhe": "mental-health",
        "mosl": "modern-slavery",
        "pl": "prison-law",
        "pub": "public-law",
        "wb": "welfare-benefits",
    }

    SLUG_TO_CATEGORY_CODE = {slug: category_code for category_code, slug in CATEGORY_CODE_TO_SLUG.items()}

    @classmethod
    def category_code_from(cls, slug):
        return CategoryManager.SLUG_TO_CATEGORY_CODE.get(slug, None)

    @classmethod
    def slug_from(cls, category_code):
        return CategoryManager.CATEGORY_CODE_TO_SLUG.get(category_code, None)
