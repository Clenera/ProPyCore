from .hooks import Hooks


class Webhooks:

    def __init__(self, access_token, server_url):
        self.hooks = Hooks(access_token, server_url)
