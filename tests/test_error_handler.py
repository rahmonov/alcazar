import pytest

from utils.tests import url


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
