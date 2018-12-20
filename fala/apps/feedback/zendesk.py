# coding=utf-8

import json
import requests
from requests.exceptions import RequestException
from django.conf import settings
from django.template import loader


ZENDESK_CUSTOM_FIELD_USERAGENT = 23791776
ZENDESK_CUSTOM_FIELD_REFERRER = 26047167
REQUEST_TIMEOUT = 10


class ZendeskClient(object):
    def feedback_payload(self, feedback_data):
        template = loader.get_template("feedback/email.html")
        feedback_body = template.render(feedback_data)

        custom_fields = []
        custom_fields.append({"id": ZENDESK_CUSTOM_FIELD_USERAGENT, "value": feedback_data["user_agent"]})
        custom_fields.append({"id": ZENDESK_CUSTOM_FIELD_REFERRER, "value": feedback_data["referrer"]})

        subject = "Find a Legal aid Adviser Feedback (FALA)"
        if settings.DEBUG:
            subject = "[TEST] - " + subject

        return {
            "ticket": {
                "requester_id": settings.ZENDESK_REQUESTER_ID,
                "subject": subject,
                "comment": {"body": feedback_body},
                "tags": ["feedback", "fala"],
                "custom_fields": custom_fields,
                "group_id": settings.ZENDESK_GROUP_ID,
            }
        }

    def create_ticket(self, feedback_data):
        return self.post("tickets", self.feedback_payload(feedback_data))

    def post(self, endpoint, data):
        try:
            response = requests.post(
                "{base}{endpoint}.json".format(base=settings.ZENDESK_API_ENDPOINT, endpoint=endpoint),
                data=json.dumps(data),
                auth=("{username}/token".format(username=settings.ZENDESK_API_USERNAME), settings.ZENDESK_API_TOKEN),
                headers={"content-type": "application/json"},
                timeout=REQUEST_TIMEOUT,
            )
        except RequestException:
            return {"json": {"error": "Timeout", "message": "Feedback request timed out."}, "status": 408}
        return {"json": response.json(), "status": response.status_code}


zendesk_client = ZendeskClient()
