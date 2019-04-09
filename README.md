<p align="center">
    <img src="https://github.com/rahmonov/alcazar/blob/master/alcazar.jpg?raw=True">
</p>

---

![purpose](https://img.shields.io/badge/purpose-learning-green.svg)
[![travis](https://travis-ci.org/rahmonov/alcazar.svg?branch=master)](https://travis-ci.org/rahmonov/alcazar)

# Alcazar

Alcazar is a Python Web Framework built for learning purposes. The plan is to learn how frameworks are built by implementing their features,
writing blog posts about them and keeping the codebase as simple as possible.

It is a WSGI framework and can be used with any WSGI application server such as Gunicorn.

## Inspiration

I was inspired to make a web framework after reading [Florimond Monca](https://twitter.com/FlorimondManca)'s [blog post](https://blog.florimondmanca.com/how-i-built-a-web-framework-and-became-an-open-source-maintainer)
about how he built a web framework and became an open source maintainer. He wrote about how thrilling the experience has been for him so I decided I would give it a try as well.
Thank you, [Florimond](https://github.com/florimondmanca) and of course [Kenneth Reitz](https://twitter.com/kennethreitz) who in turn inspired Florimond to write a framework with
his own framework [Responder](https://github.com/kennethreitz/responder). Go check out both [Bocadillo by Florimond Monca](https://github.com/bocadilloproject/bocadillo) and [Responder by Kenneth Reitz](https://github.com/kennethreitz/responder).
If you like them, show some love by staring their repos.

## Blog posts

- [Part I: Intro, API, request handlers, routing (both simple and parameterized)](http://rahmonov.me/posts/write-python-framework-part-one/)
- [Part II: class based handlers, route overlap check, unit tests](http://rahmonov.me/posts/write-python-framework-part-two/)
- [Part III: templates support, test client, django way of adding routes](http://rahmonov.me/posts/write-python-framework-part-three/)
- [Part IV: custom exception handler, support for static files, middleware](http://rahmonov.me/posts/write-python-framework-part-four/)

## Quick Start

Install it:

```bash
pip install alcazar-web-framework
```

Basic Usage:

```python
# app.py
from alcazar import Alcazar

app = Alcazar()


@app.route("/")
def home(req, resp):
    resp.text = "Hello, this is a home page."


@app.route("/about")
def about_page(req, resp):
    resp.text = "Hello, this is an about page."


@app.route("/{age:d}")
def tell_age(req, resp, age):
    resp.text = f"Your age is {age}"


@app.route("/{name:l}")
class GreetingHandler:
    def get(self, req, resp, name):
        resp.text = f"Hello, {name}"


@app.route("/show/template")
def handler_with_template(req, resp):
    resp.html = app.template("example.html", context={"title": "Awesome Framework", "body": "welcome to the future!"})


@app.route("/json")
def json_handler(req, resp):
    resp.json = {"this": "is JSON"}


@app.route("/custom")
def custom_response(req, resp):
    resp.body = b'any other body'
    resp.content_type = "text/plain"
```

Start:

```bash
gunicorn app:app
```

## Handlers

If you use class based handlers, only the methods that you implement will be allowed:

```python
@app.route("/{name:l}")
class GreetingHandler:
    def get(self, req, resp, name):
        resp.text = f"Hello, {name}"
```

This handler will only allow `GET` requests. That is, `POST` and others will be rejected. The same thing can be done with
function based handlers in the following way:

```python
@app.route("/", methods=["get"])
def home(req, resp):
    resp.text = "Hello, this is a home page."
```

Note that if you specify `methods` for class based handlers, they will be ignored.

## Unit Tests

The recommended way of writing unit tests is with [pytest](https://docs.pytest.org/en/latest/). There are two built in fixtures
that you may want to use when writing unit tests with Alcazar. The first one is `app` which is an instance of the main `Alcazar` class:

```python
def test_route_overlap_throws_exception(app):
    @app.route("/")
    def home(req, resp):
        resp.text = "Welcome Home."

    with pytest.raises(AssertionError):
        @app.route("/")
        def home2(req, resp):
            resp.text = "Welcome Home2."
```

The other one is `client` that you can use to send HTTP requests to your handlers. It is based on the famous [requests](http://docs.python-requests.org/en/master/) and it should feel very familiar:

```python
def test_parameterized_route(app, client):
    @app.route("/{name}")
    def hello(req, resp, name):
        resp.text = f"hey {name}"

    assert client.get(url("/matthew")).text == "hey matthew"
```

Note that there is a `url()` function used. It is used to generate the absolute url of the request given a relative url. Import it before usage:

```python
from alcazar.utils.tests import url
```

## Templates

The default folder for templates is `templates`. You can change it when initializing the main `Alcazar()` class:

```python
app = Alcazar(templates_dir="templates_dir_name")
```

Then you can use HTML files in that folder like so in a handler:

```python
@app.route("/show/template")
def handler_with_template(req, resp):
    resp.html = app.template("example.html", context={"title": "Awesome Framework", "body": "welcome to the future!"})
```

## Static Files

Just like templates, the default folder for static files is `static` and you can override it:

```python
app = Alcazar(static_dir="static_dir_name")
```

Then you can use the files inside this folder in HTML files:

```html
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <title>{{title}}</title>

  <link href="/static/main.css" rel="stylesheet" type="text/css">
</head>

<body>
    <h1>{{body}}</h1>
    <p>This is a paragraph</p>
</body>
</html>
```

## Custom Exception Handler

Sometimes, depending on the exception raised, you may want to do a certain action. For such cases, you can register an exception handler:

```python
def on_exception(req, resp, exception):
    if isinstance(exception, HTTPError):
        if exception.status == 404:
            resp.text = "Unfortunately the thing you were looking for was not found"
        else:
            resp.text = str(exception)
    else:
        # unexpected exceptions
        if app.debug:
            debug_exception_handler(req, resp, exception)
        else:
            print("These unexpected exceptions should be logged.")

app = Alcazar(debug=False)
app.add_exception_handler(on_exception)
```

This exception handler will catch 404 HTTPErrors and change the text to `"Unfortunately the thing you were looking for was not found"`. For other HTTPErrors, it will simply
show the exception message. If the raised exception is not an HTTPError and if `debug` is set to True, it will show the exception and its traceback. Otherwise, it will log it.

## Middleware

You can create custom middleware classes by inheriting from the `alcazar.middleware.Middleware` class and override its two methods
that are called before and after each request:

```python
from alcazar import Alcazar
from alcazar.middleware import Middleware

app = Alcazar()


class SimpleCustomMiddleware(Middleware):
    def process_request(self, req):
        print("Before dispatch", req.url)

    def process_response(self, req, res):
        print("After dispatch", req.url)


app.add_middleware(SimpleCustomMiddleware)
```

## Features

- WSGI compatible
- Basic and parameterized routing
- Class based handlers
- Test Client
- Support for templates
- Support for static files
- Custom exception handler
- Middleware

## Note

It is extremely raw and will hopefully keep improving. If you are interested in knowing how a particular feature is implemented in other
frameworks, please open an issue and we will hopefully implement and explain it in a blog post.
