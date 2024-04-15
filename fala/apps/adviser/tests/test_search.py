from django.test import Client, RequestFactory, SimpleTestCase
from django.urls import reverse

from ..views import AdviserView

# https://docs.djangoproject.com/en/5.0/topics/testing/tools/

class SearchTestWithClient(SimpleTestCase):
    '''
    Use test client to interact with views via making local web requests
    '''

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
        '''
        Bad test but just a demo of accessing context_data on the response
        '''
        response = self.client.get(self.url, { 'postcode': 'bt1 1bt' })
        form_errors = response.context_data['form'].errors  # docs mostly talk about `context` but we are `context_data`. I think cos we use jinja
        expected_message = 'This service does not cover  Northern Ireland.  Try a postcode, town or city in England or Wales.'
        self.assertEqual(form_errors, {'postcode': [expected_message]})


class SearchTestOfView(SimpleTestCase):
    '''
    Use instantiated View objects to unit test them
    '''

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_method_directly(self):
        view = AdviserView()
        context = view.get_context_data()

        self.assertEqual(context['view'].__class__, AdviserView)  # awful, atrocious test, utterly pointless and actively bad, but demonstrates calling a method