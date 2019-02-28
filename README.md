<p align="center">
    <img src="https://github.com/rahmonov/alcazar/blob/master/alcazar.jpg">
</p>

---

![purpose](https://img.shields.io/badge/purpose-learning-green.svg)

# Alcazar

Alcazar is a Python Web Framework built for learning purposes. The plan is to learn how frameworks are built by implementing their features,
writing blog posts about them and keeping the codebase as simple as possible.

It is a WSGI framework and can be used with any WSGI application server such as Gunicorn.

## Blog posts

- [Part I: Intro, API, request handlers, routing (both simple and parameterized)](http://rahmonov.me/posts/write-python-framework-part-one/)
- [Part II: class based handlers, route overlap check, unit tests](http://rahmonov.me/posts/write-python-framework-part-two/)
- [Part III: template support and etc. (to be decided)]

## Quick Start

Install it:

```bash
# TODO: pip install alcazarpy
```

Basic Usage:

```python
# app.py
from alcazar.api import API

api = API()


@api.route("/")
def home(req, resp):
    resp.text = "Hello, this is a home page."


@api.route("/about")
def about_page(req, resp):
    resp.text = "Hello, this is an about page."


@api.route("/{age:d}")
def tell_age(req, resp, age):
    resp.text = f"Your age is {age}"


@api.route("/{name:s}")
class GreetingHandler:
    def get(self, req, resp, name):
        resp.text = f"Hello, {name}"


@api.route("/show/template")
def handler_with_template(req, resp):
    resp.html = api.template("example.html", context={"title": "Awesome Framework", "body": "welcome to the future!"})


@api.route("/json")
def json_handler(req, resp):
    resp.json = {"this": "is JSON"}


@api.route("/custom")
def custom_response(req, resp):
    resp.body = b'any other body'
    resp.content_type = "text/plain"
```

Start:

```bash
gunicorn app:api
```

## Unit Tests

The recommended way of writing unit tests is with [pytest](https://docs.pytest.org/en/latest/). There are two built in fixtures
that you may want to use when writing unit tests with Alcazar. The first one is `api` which is an instance of the main `API` class:

```python
def test_route_overlap_throws_exception(api):
    @api.route("/")
    def home(req, resp):
        resp.text = "Welcome Home."

    with pytest.raises(AssertionError):
        @api.route("/")
        def home2(req, resp):
            resp.text = "Welcome Home2."
```

The other one is `client` that you can use to send HTTP requests to your handlers. It is based on the famous [requests](http://docs.python-requests.org/en/master/) and it should feel very familiar:

```python
def test_parameterized_route(api, client):
    @api.route("/{name}")
    def hello(req, resp, name):
        resp.text = f"hey {name}"

    assert client.get(url("/matthew")).text == "hey matthew"
```

Note that there is a `url()` function used. It is used to generate the absolute url of the request given a relative url. Import it before usage:

```python
from contrib.tests import url
```


## Features

- WSGI compatible
- Basic and parameterized routing
- Class based handlers
- Test Client
- Support for templates

## Coming soon

- Support for static files
- ...

## Note

It is extremely raw and will hopefully keep improving. If you are interested in knowing how a particular feature is implemented in other
frameworks, please open an issue and we will hopefully implement and explain it in a blog post.

