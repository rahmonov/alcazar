from alcazar.utils.tests import url


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


def test_status_code(app, client):
    @app.route("/cool")
    def cool(req, resp):
        resp.text = "cool thing"
        resp.status_code = 215

    assert client.get(url("/cool")).status_code == 215
