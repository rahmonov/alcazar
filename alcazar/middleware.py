from alcazar.requests import Request


class Middleware:
    def __init__(self, app):
        self.app = app

    def add(self, middleware_cls, **kwargs):
        self.app = middleware_cls(self.app, **kwargs)

    def process_request(self, req):
        pass

    def process_response(self, req, resp):
        pass

    def dispatch_request(self, request):
        self.process_request(request)
        response = self.app.dispatch_request(request)
        self.process_response(request, response)

        return response

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.app.dispatch_request(request)
        return response(environ, start_response)
