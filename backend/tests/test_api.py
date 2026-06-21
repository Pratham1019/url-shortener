from unittest.mock import patch


def test_health_returns_ok(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_post_shorten_returns_short_url(client):
    with patch("app.routes.create_short_code", return_value="abc123") as create_short_code_mock:
        response = client.post(
            "/shorten",
            json={"url": "https://example.com", "duration": 3600},
        )

    assert response.status_code == 200
    assert response.json() == {"short_url": "http://testserver/abc123"}
    create_short_code_mock.assert_called_once_with("https://example.com", 3600)


def test_get_code_redirects_when_code_exists(client):
    with patch("app.routes.get_long_url", return_value="https://example.com") as get_long_url_mock:
        response = client.get("/abc123", follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["location"] == "https://example.com"
    get_long_url_mock.assert_called_once_with("abc123")


def test_get_code_redirects_to_not_found_when_code_missing(client):
    with patch("app.routes.get_long_url", return_value=None) as get_long_url_mock:
        response = client.get("/missing", follow_redirects=False)

    assert response.status_code == 302
    assert (
        response.headers["location"]
        == "https://url-shortener-1-x8vr.onrender.com/not-found.html?code=missing"
    )
    get_long_url_mock.assert_called_once_with("missing")


def test_delete_code_returns_success_when_code_exists(client):
    with patch("app.routes.delete_short_code", return_value=True) as delete_short_code_mock:
        response = client.delete("/abc123")

    assert response.status_code == 200
    assert response.json() == {"message": "Deleted Successfully"}
    delete_short_code_mock.assert_called_once_with("abc123")


def test_delete_code_returns_404_when_code_missing(client):
    with patch("app.routes.delete_short_code", return_value=False) as delete_short_code_mock:
        response = client.delete("/missing")

    assert response.status_code == 404
    assert response.json() == {"detail": "URL not found"}
    delete_short_code_mock.assert_called_once_with("missing")
