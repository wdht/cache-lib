import json
from typing import Optional
from .cache_keys import get_default_request_cache_key


class Request:
    """Prepared request to be transmitted by transport"""

    def __init__(
        self,
        method: str,
        url: str,
        params: Optional[dict] = None,
        data=None,
        headers: Optional[dict] = None,
        content: Optional[str] = None,
        files=None,
        timeout=None,
    ):
        self.method = method.lower()
        self.url = url
        self.data = data
        self.params = params
        self.headers = headers
        self.content = content
        self.files = files
        self.timeout = timeout

    def get_cache_key(self) -> Optional[str]:
        if self.is_cacheable:
            return get_default_request_cache_key(
                self.url,
                self.method,
                self.params,
            )

    @property
    def is_cacheable(self) -> bool:
        return self.method == 'get'


class Response:
    def __init__(
        self,
        status_code: int,
        text: str,
        headers,
        original_request,
    ):
        self.status_code = status_code
        self.text = text
        if headers is None:
            self.headers = {}
        else:
            self.headers = {k.lower(): v for k, v in headers.items()}
        self.original_request = original_request

    @property
    def ok(self) -> bool:
        return self.status_code < 400

    def json(self):
        if not self.is_json:
            raise ValueError('Cannot decode JSON content for non-JSON response')
        return json.loads(self.text)

    @property
    def is_json(self) -> bool:
        if ct := self.headers.get('content-type'):
            return ct.lower() == 'application/json'
        return False
