from jinja2 import Environment, ChoiceLoader, PrefixLoader, PackageLoader


def environment(**options):
    current_loader = options["loader"]
    loader_with_govuk_frontend = ChoiceLoader(
        [current_loader, PrefixLoader({"govuk_frontend_jinja": PackageLoader("govuk_frontend_jinja")})]
    )
    options["loader"] = loader_with_govuk_frontend

    env = Environment(**options)
    return env
