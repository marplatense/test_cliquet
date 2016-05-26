from sqlalchemy.orm import configure_mappers
from test_cliquet.model import User

import pytest


@pytest.fixture(scope='session', autouse=True)
def mappers():
    configure_mappers()


def test_user_creation():
    cstruct = dict(name='Name', email='www.google.com', password='qwerty1234')
    appstruct = User.deserialize(cstruct)
    assert appstruct is not None
