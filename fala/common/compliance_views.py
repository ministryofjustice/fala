# coding=utf-8
from django.conf import settings
from django.views.generic import View
from django.http import HttpResponse
import os


class RobotsTxtView(View):
    def get(self, request):
        environment = os.getenv("ENVIRONMENT", "development").lower()

        if environment == "production":
            content = "User-agent: *\nDisallow:\n"  # Allow all
        else:
            content = "User-agent: *\nDisallow: /\n"  # Disallow all for staging/UAT

        return HttpResponse(content, content_type="text/plain")


class SecurityTxtView(View):
    def get(self, request):
        file_path = os.path.join(settings.BASE_DIR, "fala", "public", "security.txt")
        try:
            with open(file_path, "r") as f:
                content = f.read()
            return HttpResponse(content, content_type="text/plain")
        except FileNotFoundError:
            return HttpResponse("security.txt not found.", content_type="text/plain", status=404)
