import asyncio


class IHttpService:
    def __init__(self, logging, name="empty"):
        self.logger = logging.getLogger(__name__)
        self.name = name.strip()
        self.name_with_underscore = name.replace("-", "_")

    async def post_async(self, file_id, settings=None):
        await asyncio.sleep(0.01)
        return {}
