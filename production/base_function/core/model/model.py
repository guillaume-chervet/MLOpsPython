class Model:
    def __init__(self, logging, app_settings):
        self.logger = logging.getLogger(__name__)
        self.app_settings = app_settings

    def execute(self, file, filename, settings=None):
        return {
            "zones": [
                {
                    "confidence": 0.9834659099578857,
                    "coordinates": {"xmax": 411, "xmin": -9, "ymax": 1104, "ymin": -53, "file_id": "youhou"},
                    "document_id": "0",
                    "label": "Facture"
                }
            ]
        }
