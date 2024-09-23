from typing import Optional, Union
from .cache import Cache
from .models import Request, Response
from .transport_async import AiohttpTransport


class AsyncRequests:
    def __init__(self):
        self.transport = AiohttpTransport()
        self.cache = Cache()

    async def request(
        self,
        method_or_request: Union[str, Request],
        url: str = None,
        params: Optional[dict] = None,
        data=None,
        json=None,
        headers: Optional[dict] = None,
        content: Optional[str] = None,
        files=None,
        timeout=None,
        *,
        cache_timeout=None,
    ) -> Response:
        if isinstance(method_or_request, Request):
            request = method_or_request
        else:
            if not isinstance(method_or_request, str) or not isinstance(url, str):
                raise ValueError('method and url should be strings')
            request = Request(
                method_or_request,
                url,
                params,
                data,
                json,
                headers,
                content,
                files,
                timeout,
            )
        key = request.get_cache_key()
        response = self.cache.get_request(key)
        if response is None:
            response = await self.transport.perform_request(request)
            self.cache.store_response(key, response, cache_timeout)
        return response

    async def get(self, *args, **kwargs) -> Response:
        return await self.request('get', *args, **kwargs)

    async def post(self, *args, **kwargs) -> Response:
        return await self.request('post', *args, **kwargs)

    async def put(self, *args, **kwargs) -> Response:
        return await self.request('put', *args, **kwargs)

    async def delete(self, *args, **kwargs) -> Response:
        return await self.request('delete', *args, **kwargs)


async def request(
    method_or_request: Union[str, Request],
    url: str = None,
    params: Optional[dict] = None,
    data=None,
    json=None,
    headers: Optional[dict] = None,
    content: Optional[str] = None,
    files=None,
    timeout=None,
    *,
    cache_timeout=None,
):
    return await AsyncRequests().request(
        method_or_request,
        url,
        params,
        data,
        json,
        headers,
        content,
        files,
        timeout,
        cache_timeout=cache_timeout,
    )


async def get(
    url: str = None,
    params: Optional[dict] = None,
    data=None,
    json=None,
    headers: Optional[dict] = None,
    content: Optional[str] = None,
    files=None,
    timeout=None,
    *,
    cache_timeout=None,
):
    return await request(
        'get',
        url,
        params,
        data,
        json,
        headers,
        content,
        files,
        timeout,
        cache_timeout=cache_timeout,
    )


async def post(
    url: str = None,
    params: Optional[dict] = None,
    data=None,
    json=None,
    headers: Optional[dict] = None,
    content: Optional[str] = None,
    files=None,
    timeout=None,
    *,
    cache_timeout=None,
):
    return await request(
        'post',
        url,
        params,
        data,
        json,
        headers,
        content,
        files,
        timeout,
        cache_timeout=cache_timeout,
    )


async def put(
    url: str = None,
    params: Optional[dict] = None,
    data=None,
    json=None,
    headers: Optional[dict] = None,
    content: Optional[str] = None,
    files=None,
    timeout=None,
    *,
    cache_timeout=None,
):
    return await request(
        'put',
        url,
        params,
        data,
        json,
        headers,
        content,
        files,
        timeout,
        cache_timeout=cache_timeout,
    )


async def delete(
    url: str = None,
    params: Optional[dict] = None,
    data=None,
    json=None,
    headers: Optional[dict] = None,
    content: Optional[str] = None,
    files=None,
    timeout=None,
    *,
    cache_timeout=None,
):
    return await request(
        'delete',
        url,
        params,
        data,
        json,
        headers,
        content,
        files,
        timeout,
        cache_timeout=cache_timeout,
    )
