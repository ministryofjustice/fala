import unittest

from adviser.templatetags import adviser_extras


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

    def test_google_map_params(self):
        item = {
            "organisation": {"name": "The Law Org"},
            "location": {"address": "The Core, County Way Barnsley", "postcode": "S70 2JW"},
        }
        result = adviser_extras.google_map_params(item)
        self.assertEqual(result, {"api": 1, "query": "The Law Org The Core, County Way Barnsley S70 2JW"})

    def test_map_params_without_postcode(self):
        item = {"organisation": {"name": "The Law Org"}, "location": {"address": "The Core, County Way Barnsley"}}
        result = adviser_extras.google_map_params(item)
        self.assertEqual(result, {"api": 1, "query": "The Law Org The Core, County Way Barnsley"})

    def test_map_params_without_address(self):
        item = {"organisation": {"name": "The Law Org"}, "location": {"postcode": "S70 2JW"}}
        result = adviser_extras.google_map_params(item)
        self.assertEqual(result, {"api": 1, "query": "The Law Org S70 2JW"})

    def test_map_params_without_name(self):
        item = {"location": {"postcode": "S70 2JW"}}
        result = adviser_extras.google_map_params(item)
        self.assertEqual(result, {"api": 1, "query": "S70 2JW"})
