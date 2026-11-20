"""Waitlist URLs: landing, nursery QR tracking, link tracking."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("v/<slug:slug>/", views.landing_qr, name="landing-qr"),
    path("l/<slug:slug>/", views.landing_link, name="landing-link"),
]
