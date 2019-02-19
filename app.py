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
