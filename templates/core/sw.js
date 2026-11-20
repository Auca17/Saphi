{% load static %}/* Saphi service worker (M1): caches the landing shell and static assets.
   HTML is network-first; everything else is cache-first. */
const CACHE = "saphi-v1";
const SHELL = [
  "/",
  "{% static 'css/tokens.css' %}",
  "{% static 'css/fonts.css' %}",
  "{% static 'css/app.css' %}",
  "{% static 'vendor/htmx.min.js' %}",
  "{% static 'icons/icon-192.png' %}",
  "{% static 'icons/icon-512.png' %}",
];

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE).then((cache) => cache.addAll(SHELL)));
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((key) => key !== CACHE).map((key) => caches.delete(key)))
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;

  // HTML: try the network first so the form and counters stay fresh;
  // fall back to the cached shell when offline.
  if (event.request.mode === "navigate") {
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          const copy = response.clone();
          caches.open(CACHE).then((cache) => cache.put(event.request, copy));
          return response;
        })
        .catch(() => caches.match(event.request).then((hit) => hit || caches.match("/")))
    );
    return;
  }

  // Static assets (hashed in production): cache-first.
  event.respondWith(
    caches.match(event.request).then(
      (hit) =>
        hit ||
        fetch(event.request).then((response) => {
          if (response.ok && new URL(event.request.url).origin === location.origin) {
            const copy = response.clone();
            caches.open(CACHE).then((cache) => cache.put(event.request, copy));
          }
          return response;
        })
    )
  );
});
