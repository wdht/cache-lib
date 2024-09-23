from typing import Optional, Union
from .cache import Cache
from .models import Request, Response
from .transport_sync import RequestsTransport


class Requests:
    def __init__(self):
        self.transport = RequestsTransport()
        self.cache = Cache()

    def request(
        self,
        method_or_request: Union[str, Request],
        url: str = None,
        params: Optional[dict] = None,
        data=None,
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
                headers,
                content,
                files,
                timeout,
            )
        key = request.get_cache_key()
        response = self.cache.get_request(key)
        if response is None:
            response = self.transport.perform_request(request)
            self.cache.store_response(key, response, cache_timeout)
        return response

    def get(self, *args, **kwargs) -> Response:
        return self.request('get', *args, **kwargs)

    def post(self, *args, **kwargs) -> Response:
        return self.request('post', *args, **kwargs)

    def put(self, *args, **kwargs) -> Response:
        return self.request('put', *args, **kwargs)

    def delete(self, *args, **kwargs) -> Response:
        return self.request('delete', *args, **kwargs)


def request(
    method_or_request: Union[str, Request],
    url: str = None,
    params: Optional[dict] = None,
    data=None,
    headers: Optional[dict] = None,
    content: Optional[str] = None,
    files=None,
    timeout=None,
    *,
    cache_timeout=None,
):
    return Requests().request(
        method_or_request,
        url,
        params,
        data,
        headers,
        content,
        files,
        timeout,
        cache_timeout=cache_timeout,
    )


def get(
    url: str = None,
    params: Optional[dict] = None,
    data=None,
    headers: Optional[dict] = None,
    content: Optional[str] = None,
    files=None,
    timeout=None,
    *,
    cache_timeout=None,
):
    return request(
        'get',
        url,
        params,
        data,
        headers,
        content,
        files,
        timeout,
        cache_timeout=cache_timeout,
    )


def post(
    url: str = None,
    params: Optional[dict] = None,
    data=None,
    headers: Optional[dict] = None,
    content: Optional[str] = None,
    files=None,
    timeout=None,
    *,
    cache_timeout=None,
):
    return request(
        'post',
        url,
        params,
        data,
        headers,
        content,
        files,
        timeout,
        cache_timeout=cache_timeout,
    )


def put(
    url: str = None,
    params: Optional[dict] = None,
    data=None,
    headers: Optional[dict] = None,
    content: Optional[str] = None,
    files=None,
    timeout=None,
    *,
    cache_timeout=None,
):
    return request(
        'put',
        url,
        params,
        data,
        headers,
        content,
        files,
        timeout,
        cache_timeout=cache_timeout,
    )


def delete(
    url: str = None,
    params: Optional[dict] = None,
    data=None,
    headers: Optional[dict] = None,
    content: Optional[str] = None,
    files=None,
    timeout=None,
    *,
    cache_timeout=None,
):
    return request(
        'delete',
        url,
        params,
        data,
        headers,
        content,
        files,
        timeout,
        cache_timeout=cache_timeout,
    )
