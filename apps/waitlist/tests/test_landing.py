"""Landing page, visit tracking, and privacy page."""

import pytest

from apps.waitlist.models import Nursery, Visit

pytestmark = pytest.mark.django_db


@pytest.fixture
def nursery(db):
    return Nursery.objects.create(name="Vivero Los Álamos", slug="alamos", zone="maipu")


class TestLandingShell:
    def test_landing_renders_waitlist_copy(self, client):
        response = client.get("/")
        assert response.status_code == 200
        html = response.content.decode()
        assert "Planificá tu patio y enterate qué hacer cuando viene granizo" in html
        assert "Tu espacio a escala" in html
        assert "Avisos de granizo, Zonda y helada" in html
        assert "Qué sembrar cada mes" in html
        assert "Avisame por WhatsApp" in html
        assert "Acepto que Saphi me escriba por WhatsApp" in html

    def test_landing_references_manifest_and_theme(self, client):
        html = client.get("/").content.decode()
        assert 'rel="manifest" href="/manifest.webmanifest"' in html
        assert 'name="theme-color"' in html
        assert 'lang="es-AR"' in html

    def test_landing_links_to_privacy(self, client):
        html = client.get("/").content.decode()
        assert 'href="/privacidad/"' in html

    def test_privacy_page_explains_what_is_stored(self, client, settings):
        response = client.get("/privacidad/")
        assert response.status_code == 200
        html = response.content.decode()
        assert settings.FOUNDER_CONTACT_EMAIL in html
        assert "WhatsApp" in html


class TestVisitTracking:
    def test_qr_landing_records_visit_and_shows_nursery(self, client, nursery):
        response = client.get("/v/alamos/")
        assert response.status_code == 200
        assert "Te lo recomienda Vivero Los Álamos" in response.content.decode()
        visit = Visit.objects.get()
        assert visit.nursery == nursery
        assert visit.source == "qr"

    def test_link_landing_records_visit_with_link_source(self, client, nursery):
        response = client.get("/l/alamos/")
        assert response.status_code == 200
        visit = Visit.objects.get()
        assert visit.nursery == nursery
        assert visit.source == "link"

    def test_direct_landing_records_visit_without_nursery(self, client):
        client.get("/")
        visit = Visit.objects.get()
        assert visit.nursery is None
        assert visit.source == "direct"

    def test_visits_are_counted_once_per_session_per_nursery(self, client, nursery):
        client.get("/v/alamos/")
        client.get("/v/alamos/")
        assert Visit.objects.count() == 1

    def test_link_after_qr_same_nursery_counts_once(self, client, nursery):
        client.get("/v/alamos/")
        client.get("/l/alamos/")
        assert Visit.objects.count() == 1

    def test_other_nursery_counts_as_a_new_visit(self, client, nursery):
        other = Nursery.objects.create(name="Vivero Sur", slug="sur")
        client.get("/v/alamos/")
        client.get("/v/sur/")
        assert Visit.objects.count() == 2
        assert set(Visit.objects.values_list("nursery", flat=True)) == {nursery.pk, other.pk}

    def test_direct_and_qr_visits_are_separate(self, client, nursery):
        client.get("/")
        client.get("/v/alamos/")
        assert Visit.objects.count() == 2

    def test_unknown_slug_is_404(self, client):
        assert client.get("/v/no-existe/").status_code == 404
        assert client.get("/l/no-existe/").status_code == 404

    def test_inactive_nursery_is_404(self, client, nursery):
        nursery.is_active = False
        nursery.save()
        assert client.get("/v/alamos/").status_code == 404
