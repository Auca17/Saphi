"""Core URLs: health check and the privacy page."""

from django.urls import path

from . import views

urlpatterns = [
    path("healthz", views.healthz, name="healthz"),
]
