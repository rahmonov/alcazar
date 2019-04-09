import os
from whitenoise import WhiteNoise
from wsgiadapter import WSGIAdapter as RequestsWSGIAdapter
from requests import Session as RequestsSession

from .exceptions import HTTPError
from .error_handlers import debug_exception_handler
from .middleware import Middleware
from .route import Route
from .responses import Response
from .templates import get_templates_env
from .utils import empty_wsgi_app, cut_static_root, request_for_static


class Alcazar:
    def __init__(self, templates_dir="templates", static_dir="static", debug=True):
        self.templates = get_templates_env(os.path.abspath(templates_dir))
        self.static_dir = os.path.abspath(static_dir)
        self._static_root = "/static"
        self._debug = debug
        self._routes = {}
        self._exception_handler = None
        self._middleware = Middleware(self)

        # cached requests session
        self._session = None

    @property
    def debug(self):
        return self._debug

    def add_middleware(self, middleware_cls, **kwargs):
        self._middleware.add(middleware_cls, **kwargs)

    def route(self, pattern, methods=None):
        """ Decorator that adds a new route """
        def wrapper(handler):
            self.add_route(pattern, handler, methods)
            return handler

        return wrapper

    def add_route(self, pattern, handler, methods=None):
        """ Add a new route """
        assert pattern not in self._routes

        self._routes[pattern] = Route(path_pattern=pattern, handler=handler, methods=methods)

    def add_exception_handler(self, handler):
        self._exception_handler = handler

    def _handle_exception(self, request, response, exception):
        if self._exception_handler is not None:
            self._exception_handler(request, response, exception)
        else:
            if self._debug is False:
                raise exception

            debug_exception_handler(request, response, exception)

    def template(self, name, context=None):
        if context is None:
            context = {}

        return self.templates.get_template(name).render(**context)

    def dispatch_request(self, request):
        response = Response()

        route, kwargs = self.find_route(path=request.path)

        try:
            if route is None:
                raise HTTPError(status=404)

            route.handle_request(request, response, **kwargs)
        except Exception as e:
            self._handle_exception(request, response, e)

        return response

    def find_route(self, path):
        for pattern, route in self._routes.items():
            matched, kwargs = route.match(request_path=path)
            if matched is True:
                return route, kwargs

        return None, {}

    def session(self, base_url="http://testserver"):
        """Cached Testing HTTP client based on Requests by Kenneth Reitz."""
        if self._session is None:
            session = RequestsSession()
            session.mount(base_url, RequestsWSGIAdapter(self))
            self._session = session
        return self._session

    def as_whitenoise_app(self, environ, start_response):
        white_noise = WhiteNoise(empty_wsgi_app(), root=self.static_dir)
        return white_noise(environ, start_response)

    def __call__(self, environ, start_response):
        path_info = environ["PATH_INFO"]

        if request_for_static(path_info, self._static_root):
            environ["PATH_INFO"] = cut_static_root(path_info, self._static_root)
            return self.as_whitenoise_app(environ, start_response)

        return self._middleware(environ, start_response)
