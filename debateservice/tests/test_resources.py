"""
Tests of resource classes
"""
import json
from unittest import TestCase, mock

from falcon.testing import TestClient as Client
from falcon import (
    HTTPBadRequest,
    HTTPInternalServerError,
    HTTPNotFound,
    Request,
    Response
)
from requests import HTTPError

from debateservice.app import api
from debateservice.exceptions import ParseException


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
                    "author": "@someone",
                    "description": "Argument description"
                }
            ]
        }

    def test_retrieve_opinion(self, mock_scraper, mock_requests) -> None:
        """
        Test that an opinion can be retrieved
        """
        mock_scraper.return_value = self.opinion
        result = self.client.simulate_post(
            "/opinions",
            body='{"url": "http://www.debate.org/opinions/such-and-such"}',
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
            "An HTTP 200 response should have been returned."
        )

    def test_malformed_json(self, mock_scraper, mock_requests) -> None:
        """
        Test that an HTTP 400 error is returned if the request body is malformed
        """
        result = self.client.simulate_post(
            "/opinions",
            body="{NOT VALID JSON}",
            headers={"content-type": "application/json"}
        )

        self.assertEqual(
            result.status_code,
            400,
            "An HTTP 400 response should have been returned."
        )

        mock_requests.assert_not_called()
        mock_scraper.assert_not_called()

    def test_missing_url_param(self, mock_scraper, mock_requests) -> None:
        """
        Test that an HTTP 400 error is returned if request is missing the url
        """
        result = self.client.simulate_post(
            "/opinions",
            body="{}",  # <- The url is missing
            headers={"content-type": "application/json"}
        )

        self.assertEqual(
            result.status_code,
            400,
            "An HTTP 400 response should have been returned."
        )

        mock_requests.assert_not_called()
        mock_scraper.assert_not_called()

    def test_opinion_not_found(self, mock_scraper, mock_requests) -> None:
        """
        Test that an HTTP 404 error is returned if the opinion page is not found
        """
        response = mock.MagicMock()
        response.raise_for_status.side_effect = HTTPError()
        response.status_code = 404

        mock_requests.get.return_value = response

        result = self.client.simulate_post(
            "/opinions",
            body='{"url": "http://www.debate.org/opinions/such-and-such"}',
            headers={"content-type": "application/json"}
        )

        self.assertEqual(
            result.status_code,
            404,
            "An HTTP 404 response should have been returned."
        )

        mock_scraper.assert_not_called()

    def test_invalid_host(self, mock_scraper, mock_requests) -> None:
        """
        Test that an HTTP 400 error is returned if URL host is not debate.org
        """
        result = self.client.simulate_post(
            "/opinions",
            body='{"url": "http://www.google.com"}',
            headers={"content-type": "application/json"}
        )

        self.assertEqual(
            result.status_code,
            400,
            "An HTTP 400 response should have been returned."
        )

        mock_requests.assert_not_called()
        mock_scraper.assert_not_called()

    def test_parse_exception(self, mock_scraper, mock_requests) -> None:
        """
        Test that an HTTP 500 error is returned if the page cannot be parsed
        """
        mock_scraper.side_effect = ParseException()

        result = self.client.simulate_post(
            "/opinions",
            body='{"url": "http://www.debate.org/opinions/such-and-such"}',
            headers={"content-type": "application/json"}
        )

        self.assertEqual(
            result.status_code,
            500,
            "An HTTP 500 response should have been returned."
        )

    def test_unexpected_status(self, mock_scraper, mock_requests) -> None:
        """
        Test that an HTTP 500 error is returned if debate.org returns an
        unexpected status code
        """
        response = mock.MagicMock()
        response.raise_for_status.side_effect = HTTPError()
        response.status_code = 418

        mock_requests.get.return_value = response

        result = self.client.simulate_post(
            "/opinions",
            body='{"url": "http://www.debate.org/opinions/such-and-such"}',
            headers={"content-type": "application/json"}
        )

        self.assertEqual(
            result.status_code,
            500,
            "An HTTP 500 response should have been returned."
        )

        mock_scraper.assert_not_called()

    def test_unexpected_error(self, mock_scraper, mock_requests) -> None:
        """
        Test that an HTTP 500 error is returned an unexpected error occurs while
        loading the opinion page
        """
        mock_requests.get.side_effect = Exception("KaBoom!")

        result = self.client.simulate_post(
            "/opinions",
            body='{"url": "http://www.debate.org/opinions/such-and-such"}',
            headers={"content-type": "application/json"}
        )

        self.assertEqual(
            result.status_code,
            500,
            "An HTTP 500 response should have been returned."
        )

        mock_scraper.assert_not_called()
