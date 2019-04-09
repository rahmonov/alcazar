from alcazar.middleware import Middleware
from alcazar.utils import url


def test_middleware_methods_are_called(app, client):
    process_request_called = False
    process_response_called = False

    class CallMiddlewareMethods(Middleware):

        def __init__(self, app):
            super().__init__(app)

        def process_request(self, req):
            nonlocal process_request_called
            process_request_called = True

        def process_response(self, req, resp):
            nonlocal process_response_called
            process_response_called = True

    app.add_middleware(CallMiddlewareMethods)

    @app.route('/')
    def index(req, res):
        res.text = "YOLO"

    client.get(url('/'))

    assert process_request_called is True
    assert process_response_called is True
