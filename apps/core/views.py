"""Core views: health check and the privacy page."""

from django.http import HttpResponse


def healthz(request):
    """Liveness probe for Render and uptime checks."""
    return HttpResponse("ok", content_type="text/plain")
