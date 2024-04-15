from django.test import Client, RequestFactory, SimpleTestCase
from django.urls import reverse

from ..views import AdviserView

# https://docs.djangoproject.com/en/5.0/topics/testing/tools/

class SearchTestWithClient(SimpleTestCase):
    client = Client()

    # avoid hardcoding the url unless it makes sense
    # this is the name of the rule in urls.py. You can use the name of the view instead, it's a judgement call 
    url = reverse('adviser')

    def test_search_page_returns(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_michael_didnt_realise_this_was_a_get(self):
        response = self.client.post(self.url, { 'postcode': 'w1a 1aa' })
        self.assertEqual(response.status_code, 405)  # method not allowed

    def test_searching_for_a_postcode(self):
        response = self.client.get(self.url, { 'postcode': 'w1a 1aa' })
        # self.assertEqual(response.context.form.errors, ['postcode'])  # I don't know why the context isn't available on the response

        # https://docs.djangoproject.com/en/5.0/intro/tutorial05/#the-django-test-client
        # maybe we need setup_test_client()


class SearchTestOfView(SimpleTestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_searching_for_a_postcode(self):
        request = self.factory.get('/?postcode=wuuhei&name=&search=')

        response = AdviserView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        print(response.content)