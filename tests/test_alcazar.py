import pytest

import alcazar


@pytest.fixture
def api():
    return alcazar.API()


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
