import json
from django.test.runner import DiscoverRunner
from unittest import mock


def get_categories():

    with open("mock_api_categories.json", "r") as apiData:
        items = json.load(apiData)

    print(items)
    data = {item["code"].lower(): item["name"] for item in items}

    return data


def get_results_for_charles():
    return json.loads(
        """{
    "count": 4565,
    "next": "https://localhost/legal-advisers/?name=charles&page=2&postcode=W1J5BF",
    "previous": null,
    "results": [
        {
            "telephone": "0330 390 3999",
            "location": {
                "address": "50 Grosvenor Hill Mayfair\n\nLondon",
                "city": "",
                "postcode": "W1K 3QT",
                "point": {
                    "type": "Point",
                    "coordinates": [
                        -0.14545,
                        51.511368
                    ]
                },
                "type": "Outreach Office"
            },
            "organisation": {
                "name": "Disputes Mediation",
                "website": ""
            },
            "distance": 0.12459716851711009,
            "categories": [
                "FMED"
            ]
        },
        {
            "telephone": "0203 983 8880",
            "location": {
                "address": "Berkeley Square House\nBerkeley Square",
                "city": "London",
                "postcode": "W1J 6BD",
                "point": {
                    "type": "Point",
                    "coordinates": [
                        -0.144584,
                        51.509878
                    ]
                },
                "type": "Office"
            },
            "organisation": {
                "name": "Berkeley Legal",
                "website": ""
            },
            "distance": 0.12584676759598942,
            "categories": [
                "CRM"
            ]
        },
        {
            "telephone": "0203 858 0851",
            "location": {
                "address": "2Nd Floor\nBerkeley Square House\nBerkeley Square",
                "city": "London",
                "postcode": "W1J 6BD",
                "point": {
                    "type": "Point",
                    "coordinates": [
                        -0.144584,
                        51.509878
                    ]
                },
                "type": "Office"
            },
            "organisation": {
                "name": "Berkeley Square Solicitors LTD",
                "website": ""
            },
            "distance": 0.12584676759598942,
            "categories": [
                "CRM"
            ]
        },
        {
            "telephone": "0330 390 3999",
            "location": {
                "address": "2Nd Floor Berkeley Square House\n\nLondon",
                "city": "",
                "postcode": "W1J 6BD",
                "point": {
                    "type": "Point",
                    "coordinates": [
                        -0.144584,
                        51.509878
                    ]
                },
                "type": "Outreach Office"
            },
            "organisation": {
                "name": "Disputes Mediation",
                "website": ""
            },
            "distance": 0.12584676759598942,
            "categories": [
                "FMED"
            ]
        },
        {
            "telephone": "01604 345 756",
            "location": {
                "address": "3Rd Floor Berkeley Square House\nLondon",
                "city": "",
                "postcode": "W1J 6BD",
                "point": {
                    "type": "Point",
                    "coordinates": [
                        -0.144584,
                        51.509878
                    ]
                },
                "type": "Outreach Office"
            },
            "organisation": {
                "name": "Wright Mediation",
                "website": "www.wrightmediation.co.uk"
            },
            "distance": 0.12584676759598942,
            "categories": [
                "FMED"
            ]
        },
        {
            "telephone": "0208 911 8841",
            "location": {
                "address": "Suite 409\nMayfairpoint\n35 South Molton Street",
                "city": "London",
                "postcode": "W1K 5RG",
                "point": {
                    "type": "Point",
                    "coordinates": [
                        -0.148803,
                        51.514243
                    ]
                },
                "type": "Office"
            },
            "organisation": {
                "name": "Tilson Solicitors LTD",
                "website": ""
            },
            "distance": 0.29257397549560565,
            "categories": [
                "CRM"
            ]
        },
        {
            "telephone": "0330 390 3999",
            "location": {
                "address": "17 Hanover Square Mayfair\n\nLondon",
                "city": "",
                "postcode": "W1S 1BN",
                "point": {
                    "type": "Point",
                    "coordinates": [
                        -0.144726,
                        51.514289
                    ]
                },
                "type": "Outreach Office"
            },
            "organisation": {
                "name": "Disputes Mediation",
                "website": ""
            },
            "distance": 0.3136683577221526,
            "categories": [
                "FMED"
            ]
        },
        {
            "telephone": "01604 345 756",
            "location": {
                "address": "17 Hanover Square\nMayfair\nLondon",
                "city": "",
                "postcode": "W1S 1BN",
                "point": {
                    "type": "Point",
                    "coordinates": [
                        -0.144726,
                        51.514289
                    ]
                },
                "type": "Outreach Office"
            },
            "organisation": {
                "name": "Wright Mediation",
                "website": "www.wrightmediation.co.uk"
            },
            "distance": 0.3136683577221526,
            "categories": [
                "FMED"
            ]
        },
        {
            "telephone": "0333 772 0409",
            "location": {
                "address": "13 Hanover Square\nMayfair",
                "city": "London",
                "postcode": "W1S 1HN",
                "point": {
                    "type": "Point",
                    "coordinates": [
                        -0.14392,
                        51.514535
                    ]
                },
                "type": "Office"
            },
            "organisation": {
                "name": "Duncan Lewis Solicitors  LTD",
                "website": "www.dunanlewis.com"
            },
            "distance": 0.3434913667245785,
            "categories": [
                "MOSL",
                "DEB",
                "HOU"
            ]
        },
        {
            "telephone": "07812 56832",
            "location": {
                "address": "25 North Row",
                "city": "London",
                "postcode": "W1K 6DJ",
                "point": {
                    "type": "Point",
                    "coordinates": [
                        -0.154585,
                        51.513203
                    ]
                },
                "type": "Office"
            },
            "organisation": {
                "name": "Brysons Solicitors",
                "website": ""
            },
            "distance": 0.37333064114943726,
            "categories": [
                "CRM"
            ]
        }
    ],
    "origin": {
        "postcode": "W1J 5BF",
        "point": {
            "type": "Point",
            "coordinates": [
                -0.147491,
                51.510088
            ]
        }
    }
}
    """,
        strict=False,
    )


def laalaa_search(**kwargs):
    print("------------------LAALAA SEARCH START-----------------------")
    print(kwargs)
    print("------------------LAALAA SEARCH END-------------------------")
    organisation_name = kwargs.get("organisation_name")
    if organisation_name in ["test", "burns"]:
        return json.loads(
            """{
  "count": 0,
  "next": null,
  "previous": null,
  "results": []
}"""
        )

    if organisation_name == "charles":
        return get_results_for_charles()

    page = kwargs.get("page", 0)
    if isinstance(page, int) and page > 4565:
        return json.loads("""{"error": "Invalid page."}""", strict=False)

    return json.loads(
        """{
    "count": 4565,
    "next": "https://laa-legal-adviser-api-staging.apps.live-1.cloud-platform.service.justice.gov.uk/legal-advisers/?page=2",
    "previous": null,
    "results": [
        {
            "telephone": "01792 633 280",
            "location": {
                "address": "4-6 Orchard Street",
                "city": "Swansea",
                "postcode": "SA1 5AG",
                "point": {
                    "type": "Point",
                    "coordinates": [
                        -3.943112,
                        51.622156
                    ]
                },
                "type": "Office"
            },
            "organisation": {
                "name": "Public Defender Service Swansea",
                "website": ""
            },
            "categories": [
                "CRM"
            ]
        },
        {
            "telephone": "01443 629724",
            "location": {
                "address": "1 Penuel Lane",
                "city": "Pontypridd",
                "postcode": "CF37 4UF",
                "point": {
                    "type": "Point",
                    "coordinates": [
                        -3.341437,
                        51.602562
                    ]
                },
                "type": "Office"
            },
            "organisation": {
                "name": "Public Defender Service Pontypridd",
                "website": ""
            },
            "categories": [
                "CRM"
            ]
        },
        {
            "telephone": "01325 289 480",
            "location": {
                "address": "3rd Floor Stephenson House\nAlderman Best Way",
                "city": "Darlington",
                "postcode": "DL1 4WB",
                "point": {
                    "type": "Point",
                    "coordinates": [
                        -1.502321,
                        54.514943
                    ]
                },
                "type": "Office"
            },
            "organisation": {
                "name": "Public Defender Service Darlington",
                "website": ""
            },
            "categories": [
                "CRM"
            ]
        },
        {
            "telephone": "01242 548 270",
            "location": {
                "address": "Lower Ground Floor\n65 Regent House\nRodney Road",
                "city": "Cheltenham",
                "postcode": "GL50 1HX",
                "point": {
                    "type": "Point",
                    "coordinates": [
                        -2.074691,
                        51.898941
                    ]
                },
                "type": "Office"
            },
            "organisation": {
                "name": "Public Defender Service Cheltenham",
                "website": ""
            },
            "categories": [
                "CRM"
            ]
        },
        {
            "telephone": "0208 581 7403",
            "location": {
                "address": "27-37 Station Road",
                "city": "Hayes",
                "postcode": "UB3 4DX",
                "point": {
                    "type": "Point",
                    "coordinates": [
                        -0.418481,
                        51.506204
                    ]
                },
                "type": "Office"
            },
            "organisation": {
                "name": "1 Law Solicitors LTD",
                "website": ""
            },
            "categories": [
                "CRM"
            ]
        },
        {
            "telephone": "0203 011 5999",
            "location": {
                "address": "12 Caroline Street\nJewellery Quarter",
                "city": "Birmingham",
                "postcode": "B3 1TR",
                "point": {
                    "type": "Point",
                    "coordinates": [
                        -1.907137,
                        52.486093
                    ]
                },
                "type": "Office"
            },
            "organisation": {
                "name": "1 Law Solicitors LTD",
                "website": ""
            },
            "categories": [
                "CRM"
            ]
        },
        {
            "telephone": "01872 222 688",
            "location": {
                "address": "11 Edward Street",
                "city": "Truro",
                "postcode": "TR1 3AR",
                "point": {
                    "type": "Point",
                    "coordinates": [
                        -5.056496,
                        50.264714
                    ]
                },
                "type": "Office"
            },
            "organisation": {
                "name": "@Cornwall Law LLP",
                "website": ""
            },
            "categories": [
                "MAT"
            ]
        },
        {
            "telephone": "0207 231 1405",
            "location": {
                "address": "32 St Olav'S Court\nLower Road\nCanada Water",
                "city": "London",
                "postcode": "SE16 2XB",
                "point": {
                    "type": "Point",
                    "coordinates": [
                        -0.054561,
                        51.498653
                    ]
                },
                "type": "Office"
            },
            "organisation": {
                "name": "A & A Law",
                "website": ""
            },
            "categories": [
                "MOSL",
                "MAT",
                "CRM"
            ]
        },
        {
            "telephone": "0204 511 9159",
            "location": {
                "address": "85-87 Bayham Street\nCamden",
                "city": "London",
                "postcode": "NW1 0AG",
                "point": {
                    "type": "Point",
                    "coordinates": [
                        -0.140526,
                        51.537774
                    ]
                },
                "type": "Office"
            },
            "organisation": {
                "name": "Geoffrey Grace Solicitors",
                "website": ""
            },
            "categories": [
                "COM",
                "DEB",
                "MAT",
                "HOU"
            ]
        },
        {
            "telephone": "01772 888 700",
            "location": {
                "address": "58 Lancaster Road",
                "city": "Preston",
                "postcode": "PR1 1DD",
                "point": {
                    "type": "Point",
                    "coordinates": [
                        -2.698162,
                        53.760467
                    ]
                },
                "type": "Office"
            },
            "organisation": {
                "name": "A & M Solicitors LTD",
                "website": "www.aandmsolicitors.com"
            },
            "categories": [
                "CRM"
            ]
        }
    ],
    "origin": {
        "postcode": "PE30 1AA",
        "point": {
            "type": "Point",
            "coordinates": [
                0.400617,
                52.757455
            ]
        }
    }
}""",
        strict=False,
    )


class MOCKLAALAAREUNNER(DiscoverRunner):
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
