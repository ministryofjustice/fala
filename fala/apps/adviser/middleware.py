from django.conf import settings


class BlockRobotsFromStagingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if settings.BLOCK_ROBOTS:
            response["X-Robots-Tag"] = "noindex"
        return response
