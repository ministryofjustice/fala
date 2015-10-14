# -*- coding: utf-8 -*-

import json
import requests
from django.conf import settings


TICKETS_URL = 'https://ministryofjustice.zendesk.com/api/v2/tickets.json'


def auth():
    return (
        '{username}/token'.format(
            username=settings.ZENDESK_API_USERNAME),
        settings.ZENDESK_API_TOKEN
    )


def create_ticket(payload):
    return requests.post(
        TICKETS_URL,
        data=json.dumps(payload),
        auth=auth(),
        headers={'content-type': 'application/json'})


def tickets():
    return requests.get(
        TICKETS_URL,
        auth=auth())

