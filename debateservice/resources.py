"""
API Resources
"""
import json
import logging
from typing import Dict
from urllib.parse import urlparse

import requests
from requests.exceptions import HTTPError
import falcon
from falcon import Request, Response

from debateservice.scrapers import scrape_opinion_data
from debateservice.exceptions import (
    debate_org_only,
    internal_server_error,
    not_understood,
    not_found,
    missing_url_param,
    parse_error,
    ParseException
)


class OpinionResource:
    """
    Extract opinion information
    """

    def __init__(self) -> None:
        """
        Set up the OpinionResource
        """
        self.logger = logging.getLogger(__name__)

    def _extract_request_body(self, req: Request) -> Dict:
        """
        Extract the body of the request

        Parameters
        ----------
        req : Request
            The falcon request

        Parameters
        ----------
        dict
            The URL from the request body

        Raises
        ------
        HTTPBadRequest
            If the body cannot be read from the request or the body does not
            contain valid JSON
        """
        try:
            body = json.loads(req.stream.read().decode("UTF-8"))
        except:
            raise not_understood
        return body

    def _load_opinion_page(self, url: str) -> str:
        """
        Load a debate.org opinion page

        Parameters
        ----------
        url : str
            The opinion page URL to load

        Returns
        -------
        str
            The markup of the page that was loaded

        Raises
        ------
        HTTPNotFound
            If the opinion page was not found
        HTTPInternalServerError
            If an unexpected status code was received or another error occurred
            while retrieving the opinion page
        """
        try:
            resp = requests.get(url)
            resp.raise_for_status()
        except HTTPError:
            if resp.status_code == 404:
                raise not_found
            else:
                raise internal_server_error
        except:
            raise internal_server_error

        return resp.content

    def on_post(self, req: Request, resp: Response) -> None:
        """
        Retrieve opinion information from a URL

        Parameters
        ----------
        req : Request
            The falcon Request object
        resp : Response
            The falcon Response object

        Raises
        ------
        HTTPBadRequest
            If the URL parameter was missing from the request body or URL host
            is not debate.org
        """
        # Get the body from the request
        body = self._extract_request_body(req)

        # Extract the URL from body
        try:
            url = body["url"]
        except KeyError:
            raise missing_url_param

        # Ensure that the host is debate.org
        if not urlparse(url).hostname.endswith("debate.org"):
            raise debate_org_only

        # Retrieve the page
        opinion_page = self._load_opinion_page(url)

        # Extract opinion data from the page
        try:
            opinion = scrape_opinion_data(opinion_page)
        except ParseException:
            raise parse_error

        # Respond with the opinion data
        resp.body = json.dumps(opinion)
