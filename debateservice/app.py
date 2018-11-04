import json

import falcon

from debateservice.resources import OpinionResource

api = falcon.API()
api.add_route("/opinions", OpinionResource())
