from .requests import Request
from .responses import Response


class API:
    def __init__(self):
        self.routes = []

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)

        return response(environ, start_response)

    def dispatch_request(self, request):
        response = Response()
        response.text = "Hello, hard-coded World!"
        return response

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)
