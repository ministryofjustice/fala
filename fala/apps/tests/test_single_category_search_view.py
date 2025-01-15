# single_category_search.py
import re
from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings


class SingleCategorySearchViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.clinical_negligence_slug = "clinical-negligence"
        self.clinical_negligence_code = "med"
        self.welfare_benefits_slug = "welfare-benefits"
        self.welfare_benefits_code = "wb"
        self.clinical_negligence_url = reverse("single_category_search", kwargs={"category": "clinical-negligence"})
        self.welfare_benefits_url = reverse("single_category_search", kwargs={"category": "welfare-benefits"})

        settings.FEATURE_FLAG_SINGLE_CATEGORY_SEARCH_FORM = True

    def test_redirects_to_correct_category_url_clinical_negligence(self):
        response = self.client.get(
            reverse("single_category_search_query") + f"?categories={self.clinical_negligence_code}"
        )
        self.assertRedirects(response, self.clinical_negligence_url)

    def test_handles_invalid_category_code_clinical_negligence(self):
        response = self.client.get(reverse("single_category_search_query") + "?categories=invalid")
        self.assertRedirects(response, reverse("adviser"))

    def test_redirects_to_correct_category_url_welfare_benefits(self):
        response = self.client.get(
            reverse("single_category_search_query") + f"?categories={self.welfare_benefits_code}"
        )
        self.assertRedirects(response, self.welfare_benefits_url)

    def test_handles_invalid_category_code_welfare_benefits(self):
        response = self.client.get(reverse("single_category_search_query") + "?categories=invalid")
        self.assertRedirects(response, reverse("adviser"))

    def test_displays_search_form_clinical_negligence(self):
        response = self.client.get(self.clinical_negligence_url)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")

        self.assertRegex(content, re.compile(r"Find a legal aid adviser for\s+clinical negligence", re.IGNORECASE))
        self.assertRegex(
            content,
            re.compile(r"Legal aid for advice about clinical negligence is usually only available", re.IGNORECASE),
        )
        self.assertRegex(content, re.compile(r'<input type="hidden" name="categories" value="med">', re.IGNORECASE))

    def test_displays_search_form_welfare_benefits(self):
        response = self.client.get(self.welfare_benefits_url)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode("utf-8")

        self.assertRegex(content, re.compile(r"Find a legal aid adviser for\s+welfare benefits", re.IGNORECASE))
        self.assertRegex(
            content,
            re.compile(
                r"Legal aid for advice about welfare benefits is only available if you are appealing a decision made by the social security tribunal.",
                re.IGNORECASE,
            ),
        )
        self.assertRegex(content, re.compile(r'<input type="hidden" name="categories" value="wb">', re.IGNORECASE))
        self.assertRegex(
            content,
            re.compile(
                r'class="govuk-input govuk-input--width-10" id="id_postcode" name="postcode" type="text"',
                re.IGNORECASE,
            ),
        )
        self.assertRegex(
            content,
            re.compile(
                r'type="submit" class="govuk-button govuk-!-margin-bottom-2" data-module="govuk-button">\n  Search\n</button>',
                re.IGNORECASE,
            ),
        )
