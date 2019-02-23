<p align="center">
    <img src="https://github.com/rahmonov/alcazar/blob/master/alcazar.jpg">
</p>

---

![purpose](https://img.shields.io/badge/purpose-learning-green.svg)

# Alcazar

Alcazar is a Python Web Framework built for learning purposes. The plan is to learn how frameworks are built by implement their features,
writing blog posts about them and keeping the codebase as small as possible.

It is a WSGI framework and can be used with any WSGI application server such as Gunicorn.

## Blog posts

- [Part I: Intro, API, request handlers, routing (both simple and parameterized)](http://rahmonov.me/posts/write-python-framework-part-one/)
- [Part II: Test client, class based handlers, support for templates]

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
    resp.text = api.template("example.html", context={"title": "Awesome Framework", "body": "welcome to the future!"})
    resp.content_type = "text/html"
```

Start:

```bash
gunicorn app:api
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

## TODO: add a section explaining how to write unit tests with Alcazar.
     - Built in fixtures
     - Client to send an HTTP request
