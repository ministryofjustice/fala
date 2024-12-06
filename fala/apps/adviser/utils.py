# utils.py

from fala.apps.constants.categories import CATEGORY_TRANSLATIONS

SLUG_TO_CODE = {display_name: category_code for category_code, display_name in CATEGORY_TRANSLATIONS.items()}


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
