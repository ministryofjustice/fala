from enum import Enum

Region = Enum(
    "Region",
    [
        "NI",
        "IOM",
        "JERSEY",
        "GUERNSEY",
        "ENGLAND_OR_WALES",
        "SCOTLAND",
    ],
)

SCOTTISH_PREFIXES = [
    "AB",
    "DD",
    "DG",
    "EH",
    "FK",
    "G1",
    "G2",
    "G3",
    "G4",
    "G5",
    "G6",
    "G7",
    "G8",
    "G9",
    "G0",
    "HS",
    "IV",
    "KA",
    "KW",
    "KY",
    "ML",
    "PA",
    "PH",
    "TD",
    "ZE",
]

REGION_TO_LINK = {
    Region.NI: {
        "link": "https://www.nidirect.gov.uk/articles/legal-aid-schemes",
        "region": "Northern Ireland",
    },
    Region.IOM: {
        "link": "https://www.gov.im/categories/benefits-and-financial-support/legal-aid/",
        "region": "the Isle of Man",
    },
    Region.JERSEY: {
        "link": "https://www.legalaid.je/",
        "region": "Jersey",
    },
    Region.GUERNSEY: {
        "link": "https://www.gov.gg/legalaid",
        "region": "Guernsey",
    },
    Region.SCOTLAND: {
        "link": "https://www.mygov.scot/legal-aid/",
        "region": "Scotland",
    },
}
