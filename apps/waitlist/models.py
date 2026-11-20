"""Waitlist models (M1): nurseries, tracked visits, and signups.

Privacy rule (BUILD.md): store the minimum. No IP, no user agent, no
analytics cookies — a Visit is just nursery + source + timestamp, deduped
per browser session in the view.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class Zone(models.TextChoices):
    CAPITAL = "capital", _("Capital")
    GODOY_CRUZ = "godoy_cruz", _("Godoy Cruz")
    GUAYMALLEN = "guaymallen", _("Guaymallén")
    LAS_HERAS = "las_heras", _("Las Heras")
    LUJAN_DE_CUYO = "lujan_de_cuyo", _("Luján de Cuyo")
    MAIPU = "maipu", _("Maipú")
    SAN_MARTIN = "san_martin", _("San Martín")
    TUNUYAN = "tunuyan", _("Tunuyán")
    SAN_RAFAEL = "san_rafael", _("San Rafael")
    OTRA = "otra", _("Otra")


class Nursery(models.Model):
    """A nursery ("vivero") that puts a counter QR inside Saphi."""

    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, help_text=_("Used in QR and link URLs."))
    zone = models.CharField(max_length=32, choices=Zone.choices)
    contact_name = models.CharField(max_length=120, blank=True)
    contact_phone = models.CharField(max_length=32, blank=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Visit(models.Model):
    """One arrival at the landing page, deduped per session per nursery."""

    class Source(models.TextChoices):
        QR = "qr", _("QR")
        LINK = "link", _("Link")
        DIRECT = "direct", _("Direct")

    nursery = models.ForeignKey(
        Nursery,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="visits",
    )
    source = models.CharField(max_length=8, choices=Source.choices)
    created_at = models.DateTimeField(auto_now_add=True)


class Signup(models.Model):
    """A person who left their WhatsApp to hear when Saphi is ready."""

    class SpaceType(models.TextChoices):
        PATIO = "patio", _("Patio")
        BALCON = "balcon", _("Balcón")
        TERRAZA = "terraza", _("Terraza")
        HUERTA = "huerta", _("Huerta")
        SIN_ESPACIO = "sin_espacio", _("Sin espacio todavía")

    class Irrigation(models.TextChoices):
        MANGUERA = "manguera", _("Manguera")
        GOTEO = "goteo", _("Goteo")
        POR_TURNO = "por_turno", _("Por turno")
        OTRO = "otro", _("Otro")
        NO_SE = "no_se", _("No sé")

    INTEREST_CHOICES = {
        "plan": _("planificar mi espacio"),
        "weather": _("alertas de clima"),
        "sow": _("qué sembrar"),
        "buy": _("dónde comprar"),
    }

    name = models.CharField(max_length=120)
    whatsapp = models.CharField(max_length=20, unique=True)  # canonical +549... form
    zone = models.CharField(max_length=32, choices=Zone.choices)
    space_type = models.CharField(max_length=32, choices=SpaceType.choices)
    irrigation = models.CharField(max_length=32, choices=Irrigation.choices, blank=True)
    interests = models.JSONField(default=list, blank=True)
    nursery = models.ForeignKey(
        Nursery,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="signups",
    )
    source = models.CharField(max_length=8, choices=Visit.Source.choices)
    consent_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.whatsapp})"
