import inspect
from contextvars import ContextVar
from inspect import getfullargspec
from fastapi import FastAPI
from opentelemetry import trace as trace_api
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from prometheus_fastapi_instrumentator import Instrumentator

from .base_app_settings import BaseAppSettings
from .version import VERSION

IS_DEBUG_KEY = "is_debug"
_is_debug: ContextVar[bool] = ContextVar(IS_DEBUG_KEY, default=False)

IS_TRACING_ENABLED = "enable_tracing"
_is_tracing_enabled: ContextVar[bool] = ContextVar(IS_TRACING_ENABLED, default=True)


def init_tracing(base_app_settings: BaseAppSettings, fastapi_app: FastAPI = None):
    # tracing vars
    _is_debug.set(base_app_settings.is_debug)
    _is_tracing_enabled.set(base_app_settings.enable_tracing)

    # Configure collector
    if base_app_settings.use_dynatrace_collector:
        trace_exporter = OTLPSpanExporter(
            endpoint=base_app_settings.dynatrace_collector_endpoint,
            headers={"Authorization": f"Api-Token {base_app_settings.dynatrace_collector_token}"},
        )
    else:
        trace_exporter = JaegerExporter(collector_endpoint=base_app_settings.jaegger_collector_endpoint)

    span_processor = BatchSpanProcessor(trace_exporter)
    tracer_provider = TracerProvider(resource=Resource.create({SERVICE_NAME: base_app_settings.tracing_service_name}))
    tracer_provider.add_span_processor(span_processor)
    trace_api.set_tracer_provider(tracer_provider)

    # Instrument Redis
    RedisInstrumentor().instrument(tracer_provider=tracer_provider)

    # Instrument fastapi
    if fastapi_app is not None:
        FastAPIInstrumentor.instrument_app(fastapi_app, excluded_urls=base_app_settings.fastapi_excluded_urls)
        Instrumentator().instrument(fastapi_app).expose(fastapi_app)


def trace(span_name):
    """
    Method decorator to create opentelemetry span every time the async function is called.
    str :param span_name: used as span name, if the decorated method contains param with key span_name,
    its value is used, if not exist it's pulled from class attribute span_name otherwise it use span_name as name.
    Raise ValueError if decorated method is not an async function
    :return:
    """

    def trace_inner(function):
        if not inspect.iscoroutinefunction(function):
            raise ValueError(f"{function.__name__} is not an async function")

        async def trace_wrapper(*args, **kwargs):
            if not is_tracing_enabled():
                return await function(*args, **kwargs)

            args_name = getfullargspec(function).args

            if span_name in args_name:
                index = args_name.index(span_name)
                new_span_name = args[index]
            else:
                try:
                    new_span_name = getattr(args[0], span_name)
                except AttributeError:
                    new_span_name = span_name

            new_span_name = f"{function.__module__}.{new_span_name}.{function.__name__}"
            tracer = trace_api.get_tracer_provider().get_tracer(new_span_name)

            with tracer.start_as_current_span(new_span_name) as current_span:
                current_span.set_attribute("rami version", VERSION)
                if is_tracing_enabled():
                    current_span.set_attribute("input", convert_to_str(args))
                try:
                    result = await function(*args, **kwargs)
                    if is_tracing_enabled():
                        current_span.set_attribute("output", convert_to_str(result))
                except Exception as e:
                    current_span.record_exception(e)
                    raise e
                return result

        return trace_wrapper

    return trace_inner


def convert_to_str(obj) -> str:
    """
    Convert any object to tracable string
    :param obj:
    :return: string
    """
    args_as_dict = {}
    for i, j in zip(obj, range(len(obj))):
        args_as_dict[str(j + 1)] = i
    args_as_dict['args'] = obj
    return str(args_as_dict)


def is_tracing_enabled() -> bool:
    return _is_tracing_enabled.get(IS_TRACING_ENABLED)


def is_debug_mode() -> bool:
    return _is_debug.get(IS_DEBUG_KEY)
