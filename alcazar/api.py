from parse import parse

from .requests import Request
from .responses import Response


class API:
    def __init__(self):
        self.routes = {}

    def route(self, pattern):
        """
        Add a new route
        """
        def wrapper(handler):
            self.routes[pattern] = handler
            return handler

        return wrapper

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)

        return response(environ, start_response)

    def default_response(self, response):
        response.status_code = 404
        response.text = "Not found."

    def find_handler(self, path):
        for pattern, handler in self.routes.items():
            result = parse(pattern, path)
            if result is not None:
                return handler, result.named

        return None, None

    def dispatch_request(self, request):
        response = Response()

        handler, kwargs = self.find_handler(path=request.path)

        if handler is not None:
            handler(request, response, **kwargs)
        else:
            self.default_response(response)

        return response

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)
