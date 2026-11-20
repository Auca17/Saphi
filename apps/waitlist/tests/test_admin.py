"""Admin: QR downloads, signup filters + CSV export, stats view."""

import csv
import io

import pytest
from django.utils import timezone

from apps.waitlist.models import Nursery, Signup, Visit
from apps.waitlist.qr import qr_png, qr_svg, visit_url

pytestmark = pytest.mark.django_db


@pytest.fixture
def nursery(db):
    return Nursery.objects.create(name="Vivero Los Álamos", slug="alamos", zone="maipu")


@pytest.fixture
def admin_client(client):
    from django.contrib.auth.models import User

    user = User.objects.create_superuser("founder", password="test-pass-123")
    client.force_login(user)
    return client


def make_signup(**kwargs):
    defaults = {
        "name": "María",
        "whatsapp": "+5492615551234",
        "zone": "capital",
        "space_type": "patio",
        "source": "qr",
        "consent_at": timezone.now(),
    }
    return Signup.objects.create(**{**defaults, **kwargs})


class TestQr:
    def test_visit_url_targets_the_qr_landing(self, nursery):
        url = visit_url(nursery, "https://saphi.onrender.com")
        assert url == "https://saphi.onrender.com/v/alamos/"

    def test_svg_card_contains_nursery_name(self, nursery):
        svg = qr_svg(nursery, "https://saphi.onrender.com")
        assert svg.startswith("<svg")
        assert "Vivero Los Álamos" in svg
        assert "</svg>" in svg

    def test_png_card_is_a_real_png(self, nursery):
        png = qr_png(nursery, "https://saphi.onrender.com")
        assert png[:4] == b"\x89PNG"

    def test_qr_download_action_returns_png(self, admin_client, nursery):
        response = admin_client.post(
            "/admin/waitlist/nursery/",
            {"action": "download_qr_png", "_selected_action": [nursery.pk]},
            follow=False,
        )
        assert response.status_code == 200
        assert response["Content-Type"] == "image/png"
        assert "alamos" in response["Content-Disposition"]

    def test_qr_download_action_returns_svg(self, admin_client, nursery):
        response = admin_client.post(
            "/admin/waitlist/nursery/",
            {"action": "download_qr_svg", "_selected_action": [nursery.pk]},
        )
        assert response["Content-Type"] == "image/svg+xml"
        assert "Vivero" in response.content.decode()

    def test_multiple_nurseries_download_as_zip(self, admin_client, nursery):
        other = Nursery.objects.create(name="Vivero Sur", slug="sur")
        response = admin_client.post(
            "/admin/waitlist/nursery/",
            {"action": "download_qr_png", "_selected_action": [nursery.pk, other.pk]},
        )
        assert response["Content-Type"] == "application/zip"
        assert "attachment" in response["Content-Disposition"]


class TestSignupAdmin:
    def test_csv_export_action(self, admin_client, nursery):
        make_signup(nursery=nursery, interests=["weather", "sow"])
        response = admin_client.post(
            "/admin/waitlist/signup/",
            {"action": "export_csv", "_selected_action": [Signup.objects.get().pk]},
        )
        assert response["Content-Type"] == "text/csv"
        rows = list(csv.reader(io.StringIO(response.content.decode())))
        assert rows[0][:3] == ["name", "whatsapp", "zone"]
        assert "+5492615551234" in rows[1]
        assert rows[1][5] == "weather sow"

    def test_signup_list_filters_by_interest(self, admin_client, nursery):
        make_signup(interests=["weather"])
        make_signup(whatsapp="+5492615559999", interests=["plan"])
        url = "/admin/waitlist/signup/?interest=weather"
        response = admin_client.get(url)
        html = response.content.decode()
        assert "+5492615551234" in html
        assert "+5492615559999" not in html


class TestStats:
    def test_stats_view_shows_visits_signups_and_conversion(self, admin_client, nursery):
        Visit.objects.create(nursery=nursery, source="qr")
        Visit.objects.create(nursery=nursery, source="qr")
        Visit.objects.create(source="direct")
        make_signup(nursery=nursery)
        response = admin_client.get("/admin/waitlist/nursery/stats/")
        html = response.content.decode()
        assert response.status_code == 200
        assert "Vivero Los Álamos" in html
        assert "50%" in html  # 1 signup / 2 visits
        assert "Directo / sin vivero" in html

    def test_stats_requires_staff(self, client):
        response = client.get("/admin/waitlist/nursery/stats/")
        assert response.status_code == 302  # redirect to admin login
