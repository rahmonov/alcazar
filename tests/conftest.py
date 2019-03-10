import pytest

import alcazar


@pytest.fixture
def app():
    return alcazar.Alcazar(templates_dir="tests/templates", debug=False)


@pytest.fixture
def client(app):
    return app.session()
