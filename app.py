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


@api.route("/{name}")
class GreetingHandler:
    def get(self, req, resp, name):
        resp.text = f"Hello, {name}"
