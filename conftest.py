"""Shared pytest fixtures.

The production security defaults (HTTPS redirect, secure cookies) are active
whenever DEBUG is off — including under pytest — so tests opt out here to
use the plain Django test client.
"""

import pytest


@pytest.fixture(autouse=True)
def _dev_security(settings):
    settings.SECURE_SSL_REDIRECT = False
    settings.SECURE_PROXY_SSL_HEADER = None
    settings.SESSION_COOKIE_SECURE = False
    settings.CSRF_COOKIE_SECURE = False


@pytest.fixture(autouse=True)
def _plain_staticfiles(settings):
    """Use un-hashed static URLs in tests (no collectstatic needed)."""
    settings.STORAGES = {
        **settings.STORAGES,
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }
