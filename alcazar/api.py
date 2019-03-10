import os
import inspect
from parse import parse
from whitenoise import WhiteNoise
from wsgiadapter import WSGIAdapter as RequestsWSGIAdapter
from requests import Session as RequestsSession

from .exceptions import HTTPError
from .error_handlers import debug_http_error_handler
from .requests import Request
from .responses import Response
from .templates import get_templates_env


class Alcazar:
    def __init__(self, templates_dir="templates", static_dir="static", debug=True):
        self.templates = get_templates_env(os.path.abspath(templates_dir))
        self.static_dir = os.path.abspath(static_dir)
        self._routes = {}
        self._exception_handlers = []

        if debug:
            self.add_exception_handler(HTTPError, debug_http_error_handler)

        # cached requests session
        self._session = None

    def route(self, pattern):
        """ Decorator that adds a new route """
        def wrapper(handler):
            self.add_route(pattern, handler)
            return handler

        return wrapper

    def add_route(self, pattern, handler):
        """ Add a new route """
        assert pattern not in self._routes

        self._routes[pattern] = handler

    def add_exception_handler(self, exception_cls, handler):
        self._exception_handlers.insert(0, (exception_cls, handler))

    def _find_exception_handler(self, exception):
        for exception_cls, handler in self._exception_handlers:
            if isinstance(exception, exception_cls):
                return handler

    def _handle_exception(self, request, response, exception):
        exception_handler = self._find_exception_handler(exception)
        if exception_handler is None:
            raise exception

        exception_handler(request, response, exception)

    def template(self, name, context=None):
        if context is None:
            context = {}

        return self.templates.get_template(name).render(**context)

    def find_handler(self, path):
        for pattern, handler in self._routes.items():
            result = parse(pattern, path)
            if result is not None:
                return handler, result.named

        return None, None

    def dispatch_request(self, request):
        response = Response()

        handler, kwargs = self.find_handler(path=request.path)

        try:
            if handler is None:
                raise HTTPError(status=404)

            if inspect.isclass(handler):
                handler = getattr(handler(), request.method.lower(), None)
                if handler is None:
                    raise AttributeError("Method not allowed", request.method)

            handler(request, response, **kwargs)
        except Exception as e:
            self._handle_exception(request, response, e)

        return response

    def session(self, base_url="http://testserver"):
        """Cached Testing HTTP client based on Requests by Kenneth Reitz."""
        if self._session is None:
            session = RequestsSession()
            session.mount(base_url, RequestsWSGIAdapter(self))
            self._session = session
        return self._session

    def _wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)

        return response(environ, start_response)

    def as_wsgi_app(self, environ, start_response):
        white_noise = WhiteNoise(self._wsgi_app, root=self.static_dir)
        return white_noise(environ, start_response)

    def __call__(self, environ, start_response):
        return self.as_wsgi_app(environ, start_response)
