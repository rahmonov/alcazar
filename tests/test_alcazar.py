import pytest

from utils.tests import url


def test_basic_route(api):
    @api.route("/")
    def home(req, resp):
        resp.text = "Welcome Home."


def test_basic_alternative_route(api):
    def home(req, resp):
        resp.text = "Alternative way to add a route"

    api.add_route("/alternative", home)


def test_route_overlap_throws_exception(api):
    @api.route("/")
    def home(req, resp):
        resp.text = "Welcome Home."

    with pytest.raises(AssertionError):
        @api.route("/")
        def home2(req, resp):
            resp.text = "Welcome Home2."


def test_alternative_route_overlap_throws_exception(api):
    def home(req, resp):
        resp.text = "Welcome Home."

    def home2(req, resp):
        resp.text = "Welcome Home2."

    api.add_route("/alternative", home)

    with pytest.raises(AssertionError):
        api.add_route("/alternative", home2)


def test_parameterized_route(api, client):
    @api.route("/{name}")
    def hello(req, resp, name):
        resp.text = f"hey {name}"

    assert client.get(url("/matthew")).text == "hey matthew"


def test_alcazar_test_client_can_send_requests(api, client):
    RESPONSE_TEXT = "THIS IS COOL"

    @api.route("/cool")
    def cool(req, resp):
        resp.text = RESPONSE_TEXT

    assert client.get(url("/cool")).text == RESPONSE_TEXT


def test_status_code(api, client):
    @api.route("/cool")
    def cool(req, resp):
        resp.text = "cool thing"
        resp.status_code = 215

    assert client.get(url("/cool")).status_code == 215


def test_default_404_response(client):
    response = client.get(url("/doesnotexist"))

    assert response.status_code == 404
    assert response.text == "Not found."


def test_class_based_handler_route_registration(api):
    @api.route("/book")
    class BookResource:
        def get(self, req, resp):
            resp.text = "yolo"


def test_class_based_handler_get(api, client):
    response_text = "this is a get request"

    @api.route("/book")
    class BookResource:
        def get(self, req, resp):
            resp.text = response_text

    assert client.get(url("/book")).text == response_text


def test_class_based_handler_post(api, client):
    response_text = "this is a post request"

    @api.route("/book")
    class BookResource:
        def post(self, req, resp):
            resp.text = response_text

    assert client.post(url("/book")).text == response_text


def test_class_based_handler_not_allowed_method(api, client):
    @api.route("/book")
    class BookResource:
        def post(self, req, resp):
            resp.text = "yolo"

    with pytest.raises(AttributeError):
        client.get(url("/book"))


def test_json_response_helper(api, client):
    @api.route("/json")
    def json_handler(req, resp):
        resp.json = {"name": "alcazar"}

    response = client.get(url("/json"))
    json_body = response.json()

    assert response.headers["Content-Type"] == "application/json"
    assert json_body["name"] == "alcazar"


def test_html_response_helper(api, client):
    @api.route("/html")
    def html_handler(req, resp):
        resp.html = api.template("example.html", context={"title": "Best Title", "body": "Best Body"})

    response = client.get(url("/html"))

    assert "text/html" in response.headers["Content-Type"]
    assert "Best Title" in response.text
    assert "Best Body" in response.text


def test_text_response_helper(api, client):
    response_text = "Just Plain Text"

    @api.route("/text")
    def text_handler(req, resp):
        resp.text = response_text

    response = client.get(url("/text"))

    assert "text/plain" in response.headers["Content-Type"]
    assert response.text == response_text


def test_manually_setting_body(api, client):
    @api.route("/body")
    def text_handler(req, resp):
        resp.body = b"Byte Body"
        resp.content_type = "text/plain"

    response = client.get(url("/body"))

    assert "text/plain" in response.headers["Content-Type"]
    assert response.text == "Byte Body"
