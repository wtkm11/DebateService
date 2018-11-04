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
from falcon import (
    HTTPBadRequest,
    HTTPInternalServerError,
    HTTPNotFound,
    Request,
    Response
)

from debateservice.scrapers import scrape_opinion_data


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
            If the body cannot be retrieved from the request or the body does
            not contain JSON
        """
        try:
            body = json.loads(req.stream.read().decode("UTF-8"))
        except json.JSONDecodeError:
            raise HTTPBadRequest({
                "title": "Bad request",
                "description": "JSON is required."
            })
        except:
            raise HTTPBadRequest({
                "title": "Bad request",
                "description": "The request was not understood."
            })
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
                raise HTTPNotFound({
                    "title": "Not Found",
                    "description": "The opinion page does not exist."
                })
            else:
                raise HTTPInternalServerError({
                    "title": "Internal server error",
                    "description": "The opinion could not be retrieved."
                })
        except:
            raise HTTPInternalServerError({
                "title": "Internal server error",
                "description": "The opinion could not be retrieved."
            })

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
        body = self._extract_request_body(req)

        # Extract the URL from body
        try:
            url = body["url"]
        except KeyError:
            raise HTTPBadRequest({
                "title": "Bad request",
                "description": (
                    "The `url` parameter was missing from the request body."
                )
            })

        # Ensure that the host is debate.org
        if not urlparse(url).hostname.endswith("debate.org"):
            raise HTTPBadRequest({
                "title": "Bad request",
                "description": "Only debate.org URLs are supported."
            })

        # Retrieve the page
        opinion_page = self._load_opinion_page(url)

        # Extract opinion data from the page
        resp.body = json.dumps(scrape_opinion_data(opinion_page))
