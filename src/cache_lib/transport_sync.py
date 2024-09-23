from .models import Request, Response


class RequestsTransport:
    def __init__(self):
        try:
            import requests
        except ImportError:
            raise RuntimeError('requests package is unavailable')
        self.requests = requests

    def perform_request(self, request: Request) -> Response:
        response = self.requests.request(
            request.method,
            request.url,
            params=request.params,
            headers=request.headers,
            files=request.files,
            timeout=request.timeout,
        )
        return Response(
            response.status_code,
            response.text,
            response.headers,
            request,
        )
