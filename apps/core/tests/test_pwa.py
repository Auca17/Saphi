"""PWA surface: manifest, service worker, icons, vendored assets."""

import json


def test_manifest_is_served_from_root(client):
    response = client.get("/manifest.webmanifest")
    assert response.status_code == 200
    assert "json" in response["Content-Type"]

    manifest = json.loads(response.content)
    assert manifest["name"] == "Saphi"
    assert manifest["short_name"] == "Saphi"
    assert manifest["start_url"] == "/"
    assert manifest["display"] == "standalone"

    sizes = {icon["sizes"] for icon in manifest["icons"]}
    assert "192x192" in sizes
    assert "512x512" in sizes
    assert any(icon.get("purpose") == "maskable" for icon in manifest["icons"])


def test_service_worker_is_served_from_root(client):
    response = client.get("/sw.js")
    assert response.status_code == 200
    assert "javascript" in response["Content-Type"].lower()
    # Served from / so it can control the whole site scope.
    assert response.headers.get("Service-Worker-Allowed") == "/"
    assert b"saphi" in response.content


def test_icons_exist_on_disk():
    from django.conf import settings

    for name in ("icon-192.png", "icon-512.png", "icon-maskable-512.png"):
        assert (settings.BASE_DIR / "static" / "icons" / name).exists()


def test_vendored_htmx_is_committed():
    """HTMX is vendored, never loaded from a CDN at runtime."""
    from django.conf import settings

    htmx = settings.BASE_DIR / "static" / "vendor" / "htmx.min.js"
    assert htmx.exists()
    assert htmx.stat().st_size > 10_000
