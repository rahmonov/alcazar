import inspect

from parse import parse


class Route:
    def __init__(self, path_pattern, handler):
        self._path_pattern = path_pattern
        self._handler = handler

    def match(self, request_path):
        result = parse(self._path_pattern, request_path)
        if result is not None:
            return True, result.named

        return False, None

    def handle_request(self, request, response, **kwargs):
        if inspect.isclass(self._handler):
            handler = getattr(self._handler(), request.method.lower(), None)
            if handler is None:
                raise AttributeError("Method not allowed", request.method)
        else:
            handler = self._handler

        handler(request, response, **kwargs)
