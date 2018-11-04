"""
Tests of resource classes
"""
import json
from unittest import TestCase, mock

from falcon.testing import TestClient as Client

from debateservice.app import api
from debateservice.models import Opinion, Argument


@mock.patch("debateservice.resources.requests")
@mock.patch("debateservice.resources.scrape_opinion_data")
class OpinionResourceTests(TestCase):
    """
    Tests of the OpinionResource API resource
    """

    def setUp(self) -> None:
        # Create an API test client
        self.client = Client(api)

    def test_resource_calls_scraper(self, mock_scraper, mock_requests) -> None:
        """
        Test that the resource calls the scraper and returns the opinion
        """
        request_data = {
            "url": (
                "http://www.debate.org/opinions/should-drug-users-be-put-in-"
                "prison"
            )
        }
        argument = Argument(
            description="Argument description",
            author="@someone"
        )
        opinion = Opinion(
            name="Should drug users be put in jail?",
            yes_percent=42.01,
            arguments=[argument]
        )
        opinion_response = {
            "name": opinion.name,
            "yes_percent": opinion.yes_percent,
            "arguments": [
                {
                    "author": argument.author,
                    "description": argument.description
                }
            ]
        }

        mock_scraper.return_value = opinion
        result = self.client.simulate_post(
            "/opinions",
            body=json.dumps(request_data),
            headers={"content-type": "application/json"}
        )

        self.assertEqual(
            result.json,
            opinion_response,
            "The expected opinion data should have been returned"
        )

        self.assertEqual(
            result.status_code,
            200,
            "An HTTP 200 should have been returned."
        )
