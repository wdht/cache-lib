from .models import Request, Response


class AiohttpTransport:
    """
    Aiohttp-based transport.
    By default, sessions can be handled (opened and closed) internally.
    However, if session object is provided in __init__, closing it will
    be left to the caller to allow session reuse.
    """

    def __init__(self, session=None):
        try:
            import aiohttp
            self.session_class = aiohttp.ClientSession
        except ImportError:
            raise RuntimeError('aiohttp package is unavailable')
        self._provided_session = session

    async def perform_request(self, request: Request):
        if self._provided_session is None:
            response = await self._with_new_session(request)
        else:
            response = await self._make_request(self._provided_session, request)
        return Response(
            response.status_code,
            await response.text(),
            response.headers,
            request,
        )

    async def _make_request(self, session, request: Request):
        return await session.request(
            request.method,
            request.url,
            data=request.data,
            json=request.json,
            params=request.params,
            headers=request.headers,
            files=request.files,
            timeout=request.timeout,
        )

    async def _with_new_session(self, request: Request):
        async with self._default_session() as session:
            return await self._make_request(session, request)

    def _default_session(self):
        return self.session_class()
