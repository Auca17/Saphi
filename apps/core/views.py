"""Core views: health check, PWA surface, and the privacy page."""

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET


def healthz(request):
    """Liveness probe for Render and uptime checks."""
    return HttpResponse("ok", content_type="text/plain")


@require_GET
def manifest(request):
    """PWA manifest, served from the site root."""
    return render(
        request,
        "core/manifest.webmanifest",
        content_type="application/manifest+json",
    )


@require_GET
def privacy(request):
    """Plain-Spanish privacy page (what is stored, why, how to delete)."""
    return render(request, "core/privacy.html", {"founder_email": settings.FOUNDER_CONTACT_EMAIL})


@require_GET
def service_worker(request):
    """Minimal service worker. Must live at / to control the whole scope."""
    response = render(request, "core/sw.js", content_type="application/javascript")
    response["Service-Worker-Allowed"] = "/"
    response["Cache-Control"] = "no-cache"
    return response
