import unittest

from app.schemas import URLRequest


class URLRequestSchemaTestCase(unittest.TestCase):
    def test_url_request_adds_https_scheme(self) -> None:
        payload = URLRequest(url="example.com")

        self.assertEqual(payload.url, "https://example.com")

    def test_url_request_keeps_existing_scheme(self) -> None:
        payload = URLRequest(url="http://example.com")

        self.assertEqual(payload.url, "http://example.com")


if __name__ == "__main__":
    unittest.main()
