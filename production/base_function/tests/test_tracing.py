import unittest

import asyncio
from core.tracing import trace


class TestTracing(unittest.IsolatedAsyncioTestCase):

    async def test_trace_with_async_function(self):
        # Arrange
        foo = Foo("span_foo")

        # Act
        result = await foo.async_method("hello ", "world")

        # Assert
        self.assertEqual("hello world", result)


class Foo:

    def __init__(self, span_name):
        self.span = span_name

    @trace("spans")
    async def async_method(self, input1, input2):
        await asyncio.sleep(0.01)
        return input1 + input2
