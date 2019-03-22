import pytest

from utils.tests import url


def test_basic_route(app):
    @app.route("/")
    def home(req, resp):
        resp.text = "Welcome Home."


def test_basic_alternative_route(app):
    def home(req, resp):
        resp.text = "Alternative way to add a route"

    app.add_route("/alternative", home)


def test_route_overlap_throws_exception(app):
    @app.route("/")
    def home(req, resp):
        resp.text = "Welcome Home."

    with pytest.raises(AssertionError):
        @app.route("/")
        def home2(req, resp):
            resp.text = "Welcome Home2."


def test_alternative_route_overlap_throws_exception(app):
    def home(req, resp):
        resp.text = "Welcome Home."

    def home2(req, resp):
        resp.text = "Welcome Home2."

    app.add_route("/alternative", home)

    with pytest.raises(AssertionError):
        app.add_route("/alternative", home2)


def test_parameterized_route(app, client):
    @app.route("/{name}")
    def hello(req, resp, name):
        resp.text = f"hey {name}"

    assert client.get(url("/matthew")).text == "hey matthew"


def test_class_based_handler_route_registration(app):
    @app.route("/book")
    class BookResource:
        def get(self, req, resp):
            resp.text = "yolo"
