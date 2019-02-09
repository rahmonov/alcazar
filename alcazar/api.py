

class API:
    def __init__(self):
        self.routes = []

    def __call__(self, environ, start_response):
        data = b'Hello, World! I am Alcazar\n'
        status = '200 OK'
        response_headers = [
            ('Content-type', 'text/plain'),
            ('Content-Length', str(len(data)))
        ]
        start_response(status, response_headers)
        return iter([data])


api = API()
