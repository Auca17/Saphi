"""Waitlist signup form: WhatsApp normalization and Rioplatense messages."""

from django import forms
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import Signup, Zone
from .phone import normalize_whatsapp

DUPLICATE_MESSAGE = _("Ya estás anotado con ese número.")
CONSENT_MESSAGE = _("Necesitamos tu permiso para escribirte.")

_REQUIRED = {"required": _("Completá este dato.")}
_INVALID_CHOICE = {"invalid_choice": _("Elegí una opción de la lista.")}


class SignupForm(forms.Form):
    name = forms.CharField(
        max_length=120,
        error_messages=_REQUIRED | {"required": _("Decinos tu nombre.")},
    )
    whatsapp = forms.CharField(
        max_length=40,
        error_messages=_REQUIRED | {"required": _("Dejanos tu WhatsApp.")},
    )
    zone = forms.ChoiceField(
        choices=Zone.choices,
        error_messages=_REQUIRED | _INVALID_CHOICE | {"required": _("Elegí tu zona.")},
    )
    space_type = forms.ChoiceField(
        choices=Signup.SpaceType.choices,
        error_messages=_REQUIRED | _INVALID_CHOICE | {"required": _("Contanos qué espacio tenés.")},
    )
    irrigation = forms.ChoiceField(
        choices=Signup.Irrigation.choices,
        required=False,
        error_messages=_INVALID_CHOICE,
    )
    interests = forms.MultipleChoiceField(
        choices=list(Signup.INTEREST_CHOICES.items()),
        required=False,
        error_messages=_INVALID_CHOICE,
    )
    consent = forms.BooleanField(error_messages={"required": CONSENT_MESSAGE})

    def clean_whatsapp(self):
        return normalize_whatsapp(self.cleaned_data["whatsapp"])

    def clean(self):
        cleaned = super().clean()
        whatsapp = cleaned.get("whatsapp")
        if whatsapp and Signup.objects.filter(whatsapp=whatsapp).exists():
            self.add_error("whatsapp", ValidationError(DUPLICATE_MESSAGE))
        return cleaned

    def save(self, *, nursery, source):
        """Create the Signup. Returns False when the number raced us to it."""
        data = self.cleaned_data
        signup = Signup(
            name=data["name"],
            whatsapp=data["whatsapp"],
            zone=data["zone"],
            space_type=data["space_type"],
            irrigation=data.get("irrigation", ""),
            interests=data.get("interests", []),
            nursery=nursery,
            source=source,
            consent_at=timezone.now(),
        )
        try:
            signup.save()
        except IntegrityError:
            self.add_error("whatsapp", ValidationError(DUPLICATE_MESSAGE))
            return None
        return signup
