from django.db import models
from django.utils import timezone

# from django.http import Http404
# from .regions import Region
# from .laa_laa_paginator import LaaLaaPaginator
# import urllib
# from django.conf import settings


class SatisfactionFeedback(models.Model):
    satisfied = models.BooleanField(null=True, blank=True)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Feedback {self.id}"
