"""Health check used by Render (and any load balancer) to probe the app."""


def test_healthz_returns_200(client):
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.content == b"ok"
