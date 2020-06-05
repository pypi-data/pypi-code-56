import unittest
import requests_mock

from relink.client import RelinkClient


class RelinkClientTestCase(unittest.TestCase):
    @requests_mock.Mocker()
    def test_shorten_url(self, mock):
        # Given
        adapter = mock.register_uri(
            "POST",
            "https://rel.ink/api/links/",
            json={
                "hashid": "Nn8y9p",
                "url": "https://news.ycombinator.com/",
                "created_at": "2019-06-18T21:29:57.922801Z",
            },
        )

        # When
        client = RelinkClient()
        shortened_url = client.shorten_url("https://news.ycombinator.com/")

        # Then
        self.assertEqual("https://rel.ink/Nn8y9p", shortened_url)
        self.assertEqual({"url": "https://news.ycombinator.com/"}, adapter.last_request.json(),
                         "Relink API wasn't called with expected payload")

    @requests_mock.Mocker()
    def test_get_full_url(self, mock):
        # Given
        mock.register_uri(
            "GET",
            "https://rel.ink/api/links/kGXQMn/",
            json={
                "hashid": "kGXQMn",
                "url": "https://google.com/",
                "created_at": "2019-06-18T21:29:57.922801Z",
            },
        )

        # When
        client = RelinkClient()
        full_url = client.get_full_url("https://rel.ink/kGXQMn")

        # Then
        self.assertEqual("https://google.com/", full_url)


if __name__ == "__main__":
    unittest.main()
