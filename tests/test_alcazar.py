import pytest

import alcazar
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


def test_alcazar_test_client_can_send_requests(app, client):
    RESPONSE_TEXT = "THIS IS COOL"

    @app.route("/cool")
    def cool(req, resp):
        resp.text = RESPONSE_TEXT

    assert client.get(url("/cool")).text == RESPONSE_TEXT


def test_status_code(app, client):
    @app.route("/cool")
    def cool(req, resp):
        resp.text = "cool thing"
        resp.status_code = 215

    assert client.get(url("/cool")).status_code == 215


def test_class_based_handler_route_registration(app):
    @app.route("/book")
    class BookResource:
        def get(self, req, resp):
            resp.text = "yolo"


def test_class_based_handler_get(app, client):
    response_text = "this is a get request"

    @app.route("/book")
    class BookResource:
        def get(self, req, resp):
            resp.text = response_text

    assert client.get(url("/book")).text == response_text


def test_class_based_handler_post(app, client):
    response_text = "this is a post request"

    @app.route("/book")
    class BookResource:
        def post(self, req, resp):
            resp.text = response_text

    assert client.post(url("/book")).text == response_text


def test_class_based_handler_not_allowed_method(app, client):
    @app.route("/book")
    class BookResource:
        def post(self, req, resp):
            resp.text = "yolo"

    with pytest.raises(AttributeError):
        client.get(url("/book"))


def test_json_response_helper(app, client):
    @app.route("/json")
    def json_handler(req, resp):
        resp.json = {"name": "alcazar"}

    response = client.get(url("/json"))
    json_body = response.json()

    assert response.headers["Content-Type"] == "application/json"
    assert json_body["name"] == "alcazar"


def test_html_response_helper(app, client):
    @app.route("/html")
    def html_handler(req, resp):
        resp.html = app.template("example.html", context={"title": "Best Title", "body": "Best Body"})

    response = client.get(url("/html"))

    assert "text/html" in response.headers["Content-Type"]
    assert "Best Title" in response.text
    assert "Best Body" in response.text


def test_text_response_helper(app, client):
    response_text = "Just Plain Text"

    @app.route("/text")
    def text_handler(req, resp):
        resp.text = response_text

    response = client.get(url("/text"))

    assert "text/plain" in response.headers["Content-Type"]
    assert response.text == response_text


def test_manually_setting_body(app, client):
    @app.route("/body")
    def text_handler(req, resp):
        resp.body = b"Byte Body"
        resp.content_type = "text/plain"

    response = client.get(url("/body"))

    assert "text/plain" in response.headers["Content-Type"]
    assert response.text == "Byte Body"


def test_custom_error_handler(app, client):
    def on_exception(req, resp, exc):
        resp.text = "AttributeErrorHappened"

    app.add_exception_handler(on_exception)

    @app.route("/")
    def index(req, resp):
        raise AttributeError()

    response = client.get(url("/"))

    assert response.text == "AttributeErrorHappened"


def test_exception_is_propogated_if_no_exc_handler_is_defined(app, client):
    @app.route("/")
    def index(req, resp):
        raise AttributeError()

    with pytest.raises(AttributeError):
        client.get(url("/"))
