import pytest

import alcazar


@pytest.fixture
def api():
    return alcazar.API()


@pytest.fixture
def client(api):
    return api.session()
