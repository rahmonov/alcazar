import pytest

import alcazar


@pytest.fixture
def api():
    return alcazar.API()


def url(s):
    return f"http://testserver{s}"


@pytest.fixture
def client(api):
    return api.session()


def test_basic_route(api):
    @api.route("/")
    def home(req, resp):
        resp.text = "Welcome Home."


def test_route_overlap_throws_exception(api):
    @api.route("/")
    def home(req, resp):
        resp.text = "Welcome Home."

    with pytest.raises(AssertionError):
        @api.route("/")
        def home2(req, resp):
            resp.text = "Welcome Home2."


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


def test_status_code_is_returned(api, client):
    @api.route("/cool")
    def cool(req, resp):
        resp.text = "cool thing"
        resp.status_code = 215

    assert client.get(url("/cool")).status_code == 215


def test_default_404_response(client):
    response = client.get(url("/doesnotexist"))

    assert response.status_code == 404
    assert response.text == "Not found."
