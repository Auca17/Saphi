"""Waitlist views: the landing page and QR/link tracking variants."""

from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from .forms import SignupForm
from .models import Nursery, Visit


def _record_visit(request, nursery, source):
    """Store at most one Visit per session per nursery (or direct)."""
    key = nursery.slug if nursery else "direct"
    seen = request.session.setdefault("visits", [])
    if key not in seen:
        Visit.objects.create(nursery=nursery, source=source)
        seen.append(key)
        request.session.modified = True


def _is_htmx(request):
    return request.headers.get("HX-Request") == "true"


def _landing(request, nursery, source):
    context = {"nursery": nursery, "form": SignupForm(), "signup_done": False}

    if request.method == "POST":
        form = SignupForm(request.POST)
        context["form"] = form
        if form.is_valid() and form.save(nursery=nursery, source=source):
            context["signup_done"] = True
    else:
        _record_visit(request, nursery, source)

    if _is_htmx(request):
        return render(request, "waitlist/_signup_box.html", context)
    return render(request, "waitlist/landing.html", context)


@require_http_methods(["GET", "POST"])
def landing(request):
    """Direct traffic: the plain landing."""
    return _landing(request, nursery=None, source=Visit.Source.DIRECT)


@require_http_methods(["GET", "POST"])
def landing_qr(request, slug):
    """Counter QR: records a qr visit and personalizes the landing."""
    nursery = get_object_or_404(Nursery, slug=slug, is_active=True)
    return _landing(request, nursery=nursery, source=Visit.Source.QR)


@require_http_methods(["GET", "POST"])
def landing_link(request, slug):
    """Social link: same as the QR, tracked with the link source."""
    nursery = get_object_or_404(Nursery, slug=slug, is_active=True)
    return _landing(request, nursery=nursery, source=Visit.Source.LINK)
