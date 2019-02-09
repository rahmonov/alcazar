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

    def dispatch_request(self, request):
        response = Response()

        for pattern, handler in self.routes.items():
            if pattern == request.path:
                handler(request, response)
                return response

        self.default_response(response)
        return response

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)
