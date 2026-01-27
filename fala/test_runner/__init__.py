import json
import os
from django.test.runner import DiscoverRunner
from unittest import mock
from django.utils.translation import gettext_lazy as _


def _context_manager(file_path: str) -> json:
    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(path, "mock_laalaa_test_data", file_path)
    with open(path, "r") as file:
        return json.load(file)


def get_categories():

    items = _context_manager("mock_api_categories.json")
    return {item["code"].lower(): _(item["name"]) for item in items}


def get_results_for_charles():
    return _context_manager("mock_lala_company_charles.json")


def laalaa_search(**kwargs):

    organisation_name = kwargs.get("organisation_name")
    if organisation_name in ["test", "burns"]:
        return _context_manager("mock_empty_result.json")

    page = kwargs.get("page", 0)
    if isinstance(page, int) and page > 4565:
        return json.loads("""{"error": "Invalid page."}""", strict=False)

    return _context_manager("mock_lala_company_charles.json")


class FalaTestRunner(DiscoverRunner):
    def setup_test_environment(self, **kwargs):
        # This runs BEFORE the apps are fully ready for testing
        self.laala_api_client_patcher = mock.patch(
            "cla_common.laalaa.LaalaaProviderCategoriesApiClient.get_categories"
        )
        laala_api_client_mock = self.laala_api_client_patcher.start()
        laala_api_client_mock.return_value = get_categories()

        self.laalaa_search_patcher = mock.patch("fala.apps.laalaa.api.laalaa_search")
        laalaa_search_mock = self.laalaa_search_patcher.start()
        laalaa_search_mock.side_effect = laalaa_search

        super().setup_test_environment(**kwargs)

    def teardown_test_environment(self, **kwargs):
        super().teardown_test_environment(**kwargs)
        self.laala_api_client_patcher.stop()
        self.laalaa_search_patcher.stop()
