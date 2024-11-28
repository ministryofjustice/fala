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

SLUG_TO_CODE = {v: k for k, v in CATEGORY_TRANSLATIONS.items()}


def get_category_code_from_slug(slug):
    return SLUG_TO_CODE.get(slug)


def get_category_display_name(category_code):
    return CATEGORY_TRANSLATIONS.get(category_code)


CATEGORY_MESSAGES = {
    "hlpas": "Tell the adviser your home is at risk and you want advice through the Housing Loss Prevention Advice Service.",
    "welfare-benefits": (
        "Legal aid for advice about welfare benefits is only available if you are appealing a decision made by the social security tribunal. "
        "This appeal must be in the Upper Tribunal, Court of Appeal or Supreme Court.\n\n"
        "For any other benefits issue, ask the legal adviser if you can get free legal advice or if you will have to pay for it."
    ),
    "clinical-negligence": "Legal aid for advice about clinical negligence is usually only available if you have a child that suffered a brain injury during pregnancy, birth or the first 8 weeks of life.",
}

CATEGORY_DISPLAY_NAMES = {
    "hlpas": "Housing Loss Prevention Advice Service",
}
