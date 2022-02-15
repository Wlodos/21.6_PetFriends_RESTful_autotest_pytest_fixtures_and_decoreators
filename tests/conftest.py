import pytest
from settings import valid_email, valid_password
from api import pf


@pytest.fixture()
def get_key():

    status, pf.key = pf.get_api_key(valid_email, valid_password)
    assert status == 200
    assert 'key' in pf.key

    yield


@pytest.fixture()
def get_incorrect_key():

    status, pf.key = pf.get_api_key(valid_email, valid_password)
    pf.key['key'] = "invalid key"
    assert status == 200
    assert 'key' in pf.key

    yield

    assert pf.status == 403



