"""Signup form: validation rules, HTMX success state, attribution."""

import pytest

from apps.waitlist.models import Nursery, Signup

pytestmark = pytest.mark.django_db

VALID = {
    "name": "María",
    "whatsapp": "261 555 1234",
    "zone": "capital",
    "space_type": "patio",
    "irrigation": "goteo",
    "interests": ["weather", "sow"],
    "consent": "on",
}


@pytest.fixture
def nursery(db):
    return Nursery.objects.create(name="Vivero X", slug="vivero-x", zone="capital")


class TestValidationRules:
    def test_invalid_whatsapp_shows_rioplatense_error(self, client):
        response = client.post("/", {**VALID, "whatsapp": "123"})
        assert response.status_code == 200
        assert (
            "Revisá el número: tiene que ser un celular de Argentina, "
            "por ejemplo 261 555 1234." in response.content.decode()
        )
        assert Signup.objects.count() == 0

    def test_duplicate_number_shows_message_and_keeps_one_row(self, client):
        Signup.objects.create(
            name="Ana",
            whatsapp="+5492615551234",
            zone="capital",
            space_type="patio",
            consent_at="2026-01-01T00:00:00Z",
            source="direct",
        )
        response = client.post("/", VALID)
        assert response.status_code == 200
        assert "Ya estás anotado con ese número." in response.content.decode()
        assert Signup.objects.count() == 1

    def test_missing_consent_shows_error(self, client):
        data = {**VALID}
        del data["consent"]
        response = client.post("/", data)
        assert response.status_code == 200
        assert "Necesitamos tu permiso para escribirte." in response.content.decode()
        assert Signup.objects.count() == 0

    def test_missing_required_fields_show_errors(self, client):
        response = client.post("/", {"consent": "on"})
        html = response.content.decode()
        assert "Decinos tu nombre." in html
        assert "Dejanos tu WhatsApp." in html
        assert "Elegí tu zona." in html
        assert "Contanos qué espacio tenés." in html


class TestSuccess:
    def test_valid_signup_creates_row_and_shows_success(self, client):
        response = client.post("/", VALID)
        assert response.status_code == 200
        html = response.content.decode()
        assert "¡Listo!" in html
        assert "Te escribimos cuando haya novedades." in html

        signup = Signup.objects.get()
        assert signup.whatsapp == "+5492615551234"
        assert signup.zone == "capital"
        assert signup.space_type == "patio"
        assert signup.irrigation == "goteo"
        assert signup.interests == ["weather", "sow"]
        assert signup.consent_at is not None
        assert signup.source == "direct"
        assert signup.nursery is None

    def test_htmx_post_returns_only_the_signup_box_partial(self, client):
        response = client.post("/", VALID, headers={"HX-Request": "true"})
        html = response.content.decode()
        assert 'id="signup-box"' in html
        assert "¡Listo!" in html
        assert "<!doctype html>" not in html.lower()

    def test_qr_signup_is_attributed_to_the_nursery(self, client, nursery):
        response = client.post("/v/vivero-x/", VALID)
        assert response.status_code == 200
        signup = Signup.objects.get()
        assert signup.nursery == nursery
        assert signup.source == "qr"

    def test_link_signup_uses_link_source(self, client, nursery):
        client.post("/l/vivero-x/", VALID)
        assert Signup.objects.get().source == "link"

    def test_post_does_not_record_a_visit(self, client, nursery):
        from apps.waitlist.models import Visit

        client.post("/v/vivero-x/", VALID)
        assert Visit.objects.count() == 0

    def test_optional_fields_can_be_empty(self, client):
        data = {**VALID}
        del data["irrigation"], data["interests"]
        response = client.post("/", data)
        assert "¡Listo!" in response.content.decode()
        signup = Signup.objects.get()
        assert signup.irrigation == ""
        assert signup.interests == []
