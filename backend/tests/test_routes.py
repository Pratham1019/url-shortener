import os
import unittest
from unittest.mock import patch

os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")

from fastapi import HTTPException
from starlette.requests import Request

from app.routes import health_check, redirect_url, remove_url, shorten_url
from app.schemas import MessageResponse, URLRequest, URLResponse


class RoutesTestCase(unittest.TestCase):
    def make_request(self) -> Request:
        return Request(
            {
                "type": "http",
                "method": "POST",
                "scheme": "http",
                "server": ("testserver", 80),
                "path": "/shorten",
                "root_path": "",
                "headers": [],
            }
        )

    def test_health_check_returns_ok(self) -> None:
        response = health_check()

        self.assertEqual(response, {"status": "ok"})

    @patch("app.routes.create_short_code", return_value="abc123")
    def test_shorten_url_returns_generated_short_url(self, create_short_code_mock) -> None:
        response = shorten_url(
            URLRequest(url="https://example.com", duration=3600),
            self.make_request(),
        )

        self.assertIsInstance(response, URLResponse)
        self.assertEqual(response.short_url, "http://testserver/abc123")
        create_short_code_mock.assert_called_once_with("https://example.com", 3600)

    @patch("app.routes.get_long_url", return_value="https://example.com")
    def test_redirect_url_returns_redirect_for_existing_code(self, get_long_url_mock) -> None:
        response = redirect_url("abc123")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["location"], "https://example.com")
        get_long_url_mock.assert_called_once_with("abc123")

    @patch("app.routes.get_long_url", return_value=None)
    def test_redirect_url_returns_not_found_redirect_for_missing_code(self, get_long_url_mock) -> None:
        response = redirect_url("missing")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.headers["location"],
            "https://url-shortener-1-x8vr.onrender.com/not-found.html?code=missing",
        )
        get_long_url_mock.assert_called_once_with("missing")

    @patch("app.routes.delete_short_code", return_value=True)
    def test_remove_url_returns_success_message(self, delete_short_code_mock) -> None:
        response = remove_url("abc123")

        self.assertIsInstance(response, MessageResponse)
        self.assertEqual(response.message, "Deleted Successfully")
        delete_short_code_mock.assert_called_once_with("abc123")

    @patch("app.routes.delete_short_code", return_value=False)
    def test_remove_url_returns_404_for_unknown_code(self, delete_short_code_mock) -> None:
        with self.assertRaises(HTTPException) as error:
            remove_url("missing")

        self.assertEqual(error.exception.status_code, 404)
        self.assertEqual(error.exception.detail, "URL not found")
        delete_short_code_mock.assert_called_once_with("missing")


if __name__ == "__main__":
    unittest.main()
