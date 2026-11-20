"""Waitlist model behavior and constraints."""

import pytest
from django.db import IntegrityError
from django.utils import timezone

from apps.waitlist.models import Nursery, Signup, Visit

pytestmark = pytest.mark.django_db


def make_signup(**kwargs):
    defaults = {
        "name": "María",
        "whatsapp": "+5492615551234",
        "zone": "capital",
        "space_type": "patio",
        "consent_at": timezone.now(),
    }
    return Signup.objects.create(**{**defaults, **kwargs})


class TestNursery:
    def test_slug_must_be_unique(self):
        Nursery.objects.create(name="Vivero Uno", slug="vivero-uno")
        with pytest.raises(IntegrityError):
            Nursery.objects.create(name="Otro", slug="vivero-uno")

    def test_str(self):
        nursery = Nursery.objects.create(name="Vivero Los Álamos", slug="alamos")
        assert str(nursery) == "Vivero Los Álamos"


class TestSignup:
    def test_whatsapp_must_be_unique(self):
        make_signup()
        with pytest.raises(IntegrityError):
            make_signup(name="Juan")

    def test_consent_is_required(self):
        with pytest.raises(IntegrityError):
            Signup.objects.create(
                name="Sin permiso", whatsapp="+5492611112222", zone="capital", consent_at=None
            )

    def test_interests_store_a_list_of_keys(self):
        signup = make_signup(interests=["weather", "sow"])
        signup.refresh_from_db()
        assert signup.interests == ["weather", "sow"]

    def test_signup_can_reference_the_qr_nursery(self):
        nursery = Nursery.objects.create(name="Vivero X", slug="vivero-x")
        signup = make_signup(nursery=nursery, source="qr")
        assert signup.nursery == nursery
        assert signup.source == "qr"


class TestVisit:
    def test_visit_may_have_no_nursery_for_direct_traffic(self):
        visit = Visit.objects.create(source="direct", nursery=None)
        assert visit.nursery is None

    def test_source_choices(self):
        assert {c for c, _ in Visit.Source.choices} == {"qr", "link", "direct"}
