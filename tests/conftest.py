import pytest

import alcazar


@pytest.fixture
def app():
    return alcazar.Alcazar()


@pytest.fixture
def client(app):
    return app.session()
