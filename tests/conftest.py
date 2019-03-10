import pytest

import alcazar


@pytest.fixture
def app():
    return alcazar.Alcazar(templates_dir="tests/templates")


@pytest.fixture
def client(app):
    return app.session()
