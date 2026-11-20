"""Waitlist admin: nursery QR cards, signup list/CSV, per-nursery stats."""

import csv
import io
import zipfile

from django.contrib import admin
from django.db.models import Count
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.translation import gettext_lazy as _

from .models import Nursery, Signup, Visit
from .qr import qr_png, qr_svg


def _download_files(queryset, make_file, suffix, content_type):
    """Return a single file or a zip when several nurseries are selected."""
    items = [(n.slug, make_file(n)) for n in queryset]
    if len(items) == 1:
        slug, payload = items[0]
        response = HttpResponse(payload, content_type=content_type)
        response["Content-Disposition"] = f'attachment; filename="saphi-qr-{slug}.{suffix}"'
        return response

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for slug, payload in items:
            zf.writestr(f"saphi-qr-{slug}.{suffix}", payload)
    response = HttpResponse(buf.getvalue(), content_type="application/zip")
    response["Content-Disposition"] = 'attachment; filename="saphi-qrs.zip"'
    return response


@admin.register(Nursery)
class NurseryAdmin(admin.ModelAdmin):
    list_display = ("name", "zone", "is_active", "signup_count", "visit_count")
    list_filter = ("zone", "is_active")
    search_fields = ("name", "contact_name")
    prepopulated_fields = {"slug": ("name",)}
    actions = ["download_qr_png", "download_qr_svg"]
    change_list_template = "admin/waitlist/nursery_change_list.html"

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(
                _signups=Count("signups", distinct=True),
                _visits=Count("visits", distinct=True),
            )
        )

    @admin.display(description=_("Signups"), ordering="_signups")
    def signup_count(self, obj):
        return obj._signups

    @admin.display(description=_("Visits"), ordering="_visits")
    def visit_count(self, obj):
        return obj._visits

    def get_urls(self):
        stats = path(
            "stats/",
            self.admin_site.admin_view(self.stats_view),
            name="waitlist_stats",
        )
        return [stats] + super().get_urls()

    def stats_view(self, request):
        """Visits, signups and conversion per nursery (+ direct traffic)."""
        nurseries = Nursery.objects.annotate(
            _visits=Count("visits", distinct=True), _signups=Count("signups", distinct=True)
        ).order_by("-_signups", "name")

        def row(label, visits, signups):
            return {
                "label": label,
                "visits": visits,
                "signups": signups,
                "conversion": f"{signups / visits:.0%}" if visits else "—",
            }

        rows = [row(n.name, n._visits, n._signups) for n in nurseries]
        rows.append(
            row(
                _("Directo / sin vivero"),
                Visit.objects.filter(nursery__isnull=True).count(),
                Signup.objects.filter(nursery__isnull=True).count(),
            )
        )
        rows.append(
            row(
                _("Total"),
                Visit.objects.count(),
                Signup.objects.count(),
            )
        )
        return TemplateResponse(
            request,
            "admin/waitlist/stats.html",
            {**self.admin_site.each_context(request), "title": _("Estadísticas"), "rows": rows},
        )

    @admin.action(description=_("Download QR card (PNG)"))
    def download_qr_png(self, request, queryset):
        base = request.build_absolute_uri("/")
        return _download_files(queryset, lambda n: qr_png(n, base), "png", "image/png")

    @admin.action(description=_("Download QR card (SVG)"))
    def download_qr_svg(self, request, queryset):
        base = request.build_absolute_uri("/")
        return _download_files(
            queryset,
            lambda n: qr_svg(n, base).encode("utf-8"),
            "svg",
            "image/svg+xml",
        )


class InterestFilter(admin.SimpleListFilter):
    """Filter signups by a single interest key.

    JSONField contains lookups are Postgres-only, so at waitlist scale the
    match is done in Python to stay portable.
    """

    title = _("Interés")
    parameter_name = "interest"

    def lookups(self, request, model_admin):
        return list(Signup.INTEREST_CHOICES.items())

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        matching = [
            s.pk for s in queryset.only("pk", "interests") if self.value() in (s.interests or [])
        ]
        return queryset.filter(pk__in=matching)


@admin.register(Signup)
class SignupAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "whatsapp",
        "zone",
        "space_type",
        "nursery",
        "source",
        "created_at",
    )
    list_filter = ("zone", "nursery", "source", InterestFilter, "created_at")
    search_fields = ("name", "whatsapp")
    readonly_fields = ("consent_at", "created_at")
    date_hierarchy = "created_at"
    actions = ["export_csv"]

    @admin.action(description=_("Export selected signups as CSV"))
    def export_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="saphi-signups.csv"'
        writer = csv.writer(response)
        writer.writerow(
            [
                "name",
                "whatsapp",
                "zone",
                "space_type",
                "irrigation",
                "interests",
                "nursery",
                "source",
                "consent_at",
                "created_at",
            ]
        )
        for s in queryset.select_related("nursery"):
            writer.writerow(
                [
                    s.name,
                    s.whatsapp,
                    s.zone,
                    s.space_type,
                    s.irrigation,
                    " ".join(s.interests or []),
                    s.nursery.name if s.nursery else "",
                    s.source,
                    s.consent_at.isoformat(),
                    s.created_at.isoformat(),
                ]
            )
        return response
