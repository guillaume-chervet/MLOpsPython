import asyncio
from socket import AF_INET

import aiohttp
from aiohttp import TraceConfig, TraceRequestEndParams, TraceRequestStartParams
from opentelemetry.instrumentation.aiohttp_client import create_trace_config
from .tracing import convert_to_str, is_tracing_enabled, is_debug_mode

SIZE_POOL_AIOHTTP = 100

def get_trace_config() -> TraceConfig:
    trace_config = create_trace_config()
    trace_config.on_request_start.append(on_request_start)
    trace_config.on_request_end.append(on_request_end)
    return trace_config


async def on_request_start(session, trace_config_ctx, params: TraceRequestStartParams):
    if is_tracing_enabled() and is_debug_mode() \
            and trace_config_ctx is not None \
            and trace_config_ctx.span is not None:
        trace_config_ctx.span.set_attribute("headers", params.headers)
        trace_config_ctx.span.set_attribute("request", params)


async def on_request_end(session, trace_config_ctx, params: TraceRequestEndParams):
    if is_tracing_enabled() and is_debug_mode() \
            and trace_config_ctx is not None \
            and trace_config_ctx.span is not None:
        response = await params.response.read()
        trace_config_ctx.span.set_attribute("response", convert_to_str(response))


class SingletonAiohttp:
    sem: asyncio.Semaphore = None
    aiohttp_client: aiohttp.ClientSession = None

    @classmethod
    async def close(cls):
        if cls.aiohttp_client:
            await cls.aiohttp_client.close()
            cls.aiohttp_client = None

    @classmethod
    def get_aiohttp_client(cls, http_timeout) -> aiohttp.ClientSession:
        if cls.aiohttp_client is None:
            timeout = aiohttp.ClientTimeout(total=http_timeout)
            connector = aiohttp.TCPConnector(family=AF_INET, limit_per_host=SIZE_POOL_AIOHTTP)
            cls.aiohttp_client = aiohttp.ClientSession(timeout=timeout, connector=connector,
                                                       trace_configs=[get_trace_config()])

        return cls.aiohttp_client
