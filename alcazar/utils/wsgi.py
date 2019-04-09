def empty_wsgi_app():
    def wsgi(environ, start_response):
        status = '404 Not Found'
        body = b'Not Found'
        headers = [('Content-Type', 'text/plain')]
        start_response(status, headers)
        return [body]

    return wsgi
