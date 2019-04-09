import pytest

from alcazar.exceptions import HTTPError
from alcazar.utils.tests import url


def test_empty_methods(app, client):
    @app.route("/")
    def home(req, resp):
        resp.text = "Welcome Home."

    response = client.get(url("/"))

    assert response.status_code == 200


def test_only_specified_methods_are_allowed(app, client):
    @app.route("/", methods=["get"])
    def home(req, resp):
        resp.text = "Welcome Home."

    get_response = client.get(url("/"))
    assert get_response.status_code == 200

    with pytest.raises(HTTPError):
        client.post(url("/"))
