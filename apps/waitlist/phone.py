"""WhatsApp number normalization for the waitlist.

Saphi only works in Mendoza for now, so signups require an Argentine number.
phonenumbers cannot reliably tell AR mobiles from landlines (they share
area-code patterns), so any valid AR number is accepted and stored in the
canonical WhatsApp form ``+549XXXXXXXXXXX`` (the "9" marks a mobile when
dialing internationally — WhatsApp needs it, and keeping one canonical form
makes the unique constraint dedupe the two ways of writing the same line).
"""

import phonenumbers
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

INVALID_MESSAGE = _(
    "Revisá el número: tiene que ser un celular de Argentina, por ejemplo 261 555 1234."
)


def normalize_whatsapp(raw: str) -> str:
    """Return the canonical E.164 form of an Argentine number.

    Raises ValidationError (with the Rioplatense UI message) when the input
    is not a valid number in Argentina.
    """
    try:
        parsed = phonenumbers.parse((raw or "").strip(), "AR")
    except phonenumbers.NumberParseException:
        raise ValidationError(INVALID_MESSAGE) from None

    if parsed.country_code != 54 or not phonenumbers.is_valid_number(parsed):
        raise ValidationError(INVALID_MESSAGE)

    e164 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
    if e164.startswith("+549"):
        return e164
    return "+549" + e164[3:]
