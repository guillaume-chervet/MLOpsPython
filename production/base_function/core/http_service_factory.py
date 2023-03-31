from .http_service import HttpService


class HttpServiceFactory:
    def __init__(self, logging):
        self.logging = logging

    def create(self, name="empty"):
        return HttpService(self.logging, name)
