"""
Tests of resource classes
"""
import json
from unittest import TestCase, mock

from falcon.testing import TestClient as Client

from debateservice.app import api


@mock.patch("debateservice.resources.requests")
@mock.patch("debateservice.resources.scrape_opinion_data")
class OpinionResourceTests(TestCase):
    """
    Tests of the OpinionResource API resource
    """

    def setUp(self) -> None:
        # Create an API test client
        self.client = Client(api)
        self.opinion = {
            "name": "Should drug users be put in jail?",
            "yes_percent": 42.01,
            "arguments": [
                {
                    "author": "Argument description",
                    "description": "@someone"
                }
            ]
        }

    def test_retrieve_opinion(self, mock_scraper, mock_requests) -> None:
        """
        Test that an opinion can be retrieved
        """
        request_data = {
            "url": (
                "http://www.debate.org/opinions/should-drug-users-be-put-in-"
                "prison"
            )
        }

        mock_scraper.return_value = self.opinion
        result = self.client.simulate_post(
            "/opinions",
            body=json.dumps(request_data),
            headers={"content-type": "application/json"}
        )

        self.assertEqual(
            result.json,
            self.opinion,
            "The expected opinion data should have been returned"
        )

        self.assertEqual(
            result.status_code,
            200,
            "An HTTP 200 should have been returned."
        )
