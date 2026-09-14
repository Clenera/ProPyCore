from .hooks import Hooks
from .triggers import Triggers


class Webhooks:

    def __init__(self, access_token, server_url):
        self.hooks = Hooks(access_token, server_url)
        self.triggers = Triggers(access_token, server_url)
