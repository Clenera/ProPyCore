from .hooks import Hooks
from .triggers import Triggers
from .resources import Resources


class Webhooks:

    def __init__(self, access_token, server_url):
        self.hooks = Hooks(access_token, server_url)
        self.triggers = Triggers(access_token, server_url)
        self.resources = Resources(access_token, server_url)
