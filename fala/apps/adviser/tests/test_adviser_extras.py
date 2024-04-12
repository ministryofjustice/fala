import unittest

from fala.apps.adviser.templatetags import adviser_extras


class QueryToDictTest(unittest.TestCase):
    def test_returns_the_parsed_query_parameters_when_no_prop_is_given(self):
        result = adviser_extras.query_to_dict("irrelevant", "http://localhost:8000/?postcode=SW1A&page=3")
        self.assertEqual({"postcode": ["SW1A"], "page": ["3"]}, result)

    def test_returns_the_value_of_a_query_parameter_when_a_prop_is_given(self):
        result = adviser_extras.query_to_dict("irrelevant", "http://localhost:8000/?postcode=SW1A&page=3", "page")
        self.assertEqual(["3"], result)

    def test_returns_an_empty_list_when_a_prop_is_given_but_does_not_exist(self):
        result = adviser_extras.query_to_dict("irrelevant", "http://localhost:8000/?postcode=SW1A&page=3", "potato")
        self.assertEqual([], result)
