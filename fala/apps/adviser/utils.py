# utils.py

CATEGORY_TRANSLATIONS = {
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
    "hlpas": "hlpas",
    "immas": "immigration-asylum",
    "mhe": "mental-health",
    "mosl": "modern-slavery",
    "pl": "prison-law",
    "pub": "public-law",
    "wb": "welfare-benefits",
}


def get_category_display_name(category_code):
    return CATEGORY_TRANSLATIONS.get(category_code)
