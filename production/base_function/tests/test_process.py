import logging
import unittest

from core.http_service_factory import HttpServiceFactory
from core.model.app_settings import AppSettings
from core.model.model import Model
from core.post_processing.post_processing import PostProcessing
from core.post_processing.post_processing_app_settings import PostProcessingAppSettings
from core.pre_processing.pre_processing import PreProcessing
from core.pre_processing.pre_processing_app_settings import PreProcessingAppSettings
from core.process import Process
from opentelemetry.sdk.trace import export
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from tests.redis_mock import RedisMock
from unittest.mock import MagicMock
from opentelemetry import trace as trace_api
from opentelemetry.sdk import trace


class TestProcess(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        tracer_provider = trace.TracerProvider()
        trace_api.set_tracer_provider(tracer_provider)
        span_processor = export.SimpleSpanProcessor(InMemorySpanExporter())
        tracer_provider.add_span_processor(span_processor)

    async def test_process(self):
        redis = RedisMock(logging)
        http_service_factory = HttpServiceFactory(logging)
        post_processing = PostProcessing(logging, PostProcessingAppSettings(logging), redis, http_service_factory)
        pre_processing = PreProcessing(logging, PreProcessingAppSettings(logging), redis)
        model = Model(logging, AppSettings(logging))
        process = Process(logging, redis, model, pre_processing, post_processing)

        result = await process.process_document_async(None, "test.png")

        expected_result = {
            'zones': [
                {
                    'confidence': 0.9834659099578857,
                    'coordinates': {'xmax': 411, 'xmin': -9, 'ymax': 1104, 'ymin': -53, 'file_id': 'youhou'},
                    'document_id': '0',
                    'label': 'Facture',
                }
            ]
        }

        self.assertEqual(
            expected_result,
            result,
        )

    async def test_process_with_exception(self):
        redis = RedisMock(logging)
        http_service_factory = HttpServiceFactory(logging)

        pre_processing = PreProcessing(logging, PreProcessingAppSettings(logging), redis)

        expected_result = {}

        async def async_func():
            return expected_result

        post_processing = PostProcessing(logging, PostProcessingAppSettings(logging), redis, http_service_factory)
        post_processing.on_exception_async = MagicMock(async_func)

        model = Model(logging, AppSettings(logging))
        model.execute = MagicMock()
        model.execute.side_effect = Exception('Boom!')

        process = Process(logging, redis, model, pre_processing, post_processing)
        with self.assertRaises(Exception) as cm:
            await process.process_document_async(None, "test.png")
        self.assertEqual('Boom!', str(cm.exception))
        post_processing.on_exception_async.assert_called()
