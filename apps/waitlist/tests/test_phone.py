"""WhatsApp normalization rules (BUILD.md M1 validation rules)."""

import pytest
from django.core.exceptions import ValidationError

from apps.waitlist.phone import normalize_whatsapp


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("261 555 1234", "+5492615551234"),  # national format, Mendoza
        ("2615551234", "+5492615551234"),
        ("+54 9 261 555-1234", "+5492615551234"),  # already international mobile
        ("+5492615551234", "+5492615551234"),
    ],
)
def test_valid_argentine_numbers_normalize_to_canonical_e164(raw, expected):
    assert normalize_whatsapp(raw) == expected


def test_national_and_international_forms_of_the_same_mobile_dedupe():
    assert normalize_whatsapp("261 555 1234") == normalize_whatsapp("+54 9 261 555 1234")


@pytest.mark.parametrize("raw", ["11234567", "261 555 123", "abcdef", "", "12"])
def test_invalid_numbers_raise_validation_error(raw):
    with pytest.raises(ValidationError) as exc:
        normalize_whatsapp(raw)
    assert "Revisá el número" in str(exc.value)


def test_non_argentine_numbers_are_rejected():
    with pytest.raises(ValidationError):
        normalize_whatsapp("+44 7911 123456")  # valid UK mobile, but not AR
