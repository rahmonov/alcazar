import pytest

from utils import request_for_static, cut_static_root


@pytest.mark.parametrize(
    "request_path, is_request_for_static",
    [
        ("/static/main.css", True),
        ("/static/vendor/alert.js", True),
        ("/home", False),
        ("/books/13", False),
    ]
)
def test_request_for_static(request_path, is_request_for_static):
    assert request_for_static(request_path, "/static") is is_request_for_static


def test_cut_static_root():
    result = cut_static_root("/static/main.css", "/static")

    assert result == "/main.css"


def test_cut_static_root_raises_exception_if_request_path_is_not_for_static():
    with pytest.raises(AssertionError):
        cut_static_root("/home/about", "/static")
