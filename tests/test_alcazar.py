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


def test_alcazar_test_client_can_send_requests(api, client):
    RESPONSE_TEXT = "THIS IS COOL"

    @api.route("/hey")
    def cool(req, resp):
        resp.text = RESPONSE_TEXT

    assert client.get(url("/hey")).text == RESPONSE_TEXT
