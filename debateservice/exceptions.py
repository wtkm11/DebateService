"""
DebateService exceptions
"""
from falcon import (
    HTTPBadRequest,
    HTTPInternalServerError,
    HTTPNotFound
)


class ParseException(Exception):
    """
    An exception to raise if an error occurs while parsing an opinion page
    """

parse_error = HTTPInternalServerError({
    "title": "Internal server error",
    "description": "The opinion could not be parsed."
})

not_understood = HTTPBadRequest({
    "title": "Bad request",
    "description": "The request was not understood."
})

not_found = HTTPNotFound()

internal_server_error = HTTPInternalServerError({
    "title": "Internal server error",
    "description": "The opinion could not be retrieved."
})

missing_url_param = HTTPBadRequest({
    "title": "Bad request",
    "description": (
        "The `url` parameter was missing from the request body."
    )
})

debate_org_only = HTTPBadRequest({
    "title": "Bad request",
    "description": "Only debate.org URLs are supported."
})
