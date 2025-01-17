from jinja2 import Environment, ChoiceLoader, PrefixLoader, PackageLoader
from django.utils import translation


def environment(**options):
    current_loader = options["loader"]
    loader_with_govuk_frontend = ChoiceLoader(
        [current_loader, PrefixLoader({"govuk_frontend_jinja": PackageLoader("govuk_frontend_jinja")})]
    )
    options["loader"] = loader_with_govuk_frontend
    options["extensions"] = options.get("extensions", []) + ["jinja2.ext.i18n"]

    env = Environment(**options)
    env.install_gettext_translations(translation)
    return env
