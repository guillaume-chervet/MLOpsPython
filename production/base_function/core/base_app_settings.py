import os

from pathlib import Path

from .model.name import NAME


class BaseAppSettings:
    def __init__(self, logging):
        self.logger = logging.getLogger(__name__)
        self.orchestrator_timeout_second = int(os.getenv("orchestrator_timeout_second", 60))
        self.is_debug = os.getenv("log_level", "WARNING").upper() == "DEBUG"
        self.enable_tracing = os.getenv("ENABLE_TRACING", "false").lower() == 'true'
        self.use_dynatrace_collector = os.getenv("USE_DYNATRACE_COLLECTOR", "false").lower() == 'true'
        self.tracing_service_name = os.getenv("TRACING_SERVICE_NAME", NAME)
        self.jaegger_collector_endpoint = os.getenv("EXPORTER_JAEGER_ENDPOINT")
        self.dynatrace_collector_endpoint = os.getenv("EXPORTER_DYNATRACE_ENDPOINT")
        self.dynatrace_token_path = os.getenv("DYNATRACE_TOKEN_PATH")
        self.fastapi_excluded_urls = os.getenv("OTEL_PYTHON_FASTAPI_EXCLUDED_URLS", "version,health,metrics,docs*")
        self.client_url_file = os.getenv("client_url_file", "http://localhost:5009/{id}")
        # Check mandatory tracing var env:
        errors = []
        if self.enable_tracing and self.use_dynatrace_collector:
            if not self.dynatrace_collector_endpoint:
                errors.append(
                    "Dynatrace endpoint should not be empty or None! Check var env EXPORTER_DYNATRACE_ENDPOINT")
            if not self.dynatrace_token_path:
                errors.append(
                    "Dynatrace authentication token path should not be empty or None! "
                    "Check var env DYNATRACE_TOKEN_PATH")
            if not Path(self.dynatrace_token_path).exists():
                errors.append(
                    "Dynatrace authentication token path does not exist! "
                    f"Check path {self.dynatrace_token_path}")
            with open(self.dynatrace_token_path) as dynatrace_token_file:
                self.dynatrace_collector_token = dynatrace_token_file.read()
            if not self.dynatrace_collector_token:
                errors.append(
                    "Dynatrace authentication token should not be empty or None! Check var env EXPORTER_DYNATRACE_TOKEN")
        if self.enable_tracing and not self.use_dynatrace_collector and not self.jaegger_collector_endpoint:
            errors.append(
                "JAEGER endpoint should not be empty or None! Check var env EXPORTER_JAEGER_ENDPOINT")
        if errors:
            raise ValueError('\n'.join(errors))
