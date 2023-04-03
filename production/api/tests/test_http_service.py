import logging
import unittest
from unittest.mock import patch

from opentelemetry import trace as trace_api
from opentelemetry.sdk.trace import TracerProvider, export
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

from base_function.core.base_app_settings import BaseAppSettings
from base_function.core.http_service import HttpService
from base_function.core.tracing import init_tracing


def http_service_post_async(logger, data, url, number_retry=0, current_retry_number=0, http_timeout=30):
    return {
        'logger': logger.name,
        'data': data,
        'url': url,
        'number_retry': number_retry,
        'current_retry_number': current_retry_number,
        'http_timeout': http_timeout
    }


def make_coroutine(function_to_convert):
    async def coroutine(*args, **kwargs):
        return function_to_convert(*args, **kwargs)

    return coroutine


class TestHttpService(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        # mock post_async function
        self.patcher = patch('base_function.core.http_service.post_async',
                             new=make_coroutine(http_service_post_async))
        self.patcher.start()

        # init tracing
        settings = BaseAppSettings(logging)
        settings.is_debug = True
        init_tracing(settings)

        # Setup trace
        tracer_provider = TracerProvider()
        trace_api.set_tracer_provider(tracer_provider)
        span_processor = export.SimpleSpanProcessor(InMemorySpanExporter())
        tracer_provider.add_span_processor(span_processor)

    def tearDown(self):
        self.patcher.stop()

    async def test_post_async(self):
        # Arrange
        test_http_service = HttpService(logging, "test_http_service")
        expected = {'current_retry_number': 0,
                    'data': {'id': 'file_id',
                             'settings': {'action': 'test_http_service', 'mail_json_id': 'mail_json_id'}},
                    'http_timeout': 30,
                    'logger': 'base_function.core.i_http_service',
                    'number_retry': 3,
                    'url': 'http://gateway/async-function/test-http-service?sync=false'}

        # Act
        result = await test_http_service.post_async('file_id', {"mail_json_id": 'mail_json_id'})

        # Assert
        self.assertEqual(expected, result)
