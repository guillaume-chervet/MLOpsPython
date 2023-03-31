from .model import Model


class ModelFactory:
    def __init__(self, logging, app_settings):
        self.logging = logging
        self.app_settings = app_settings

    def create(self):
        return Model(self.logging, self.app_settings)
