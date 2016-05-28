import colander
import pytest
from sqlalchemy.orm import configure_mappers


from test_cliquet.model import User


@pytest.fixture(scope='session', autouse=True)
def mappers():
    configure_mappers()


def error_lookup(searched_attribute, invalid_errors, message=None):
    for err in invalid_errors.value.children:
        if searched_attribute == err.node.name:
            return message is None or (message is not None and err.msg == message or message in err.msg)
    return False


def test_deserialize_ok():
    """
    Basic deserialization
    """
    cstruct = dict(email='user@example.com', password='abc:qwerty1234', name='Name')
    appstruct = User.deserialize(cstruct)
    assert appstruct.name == 'Name'
    assert appstruct.email == 'user@example.com'
    assert isinstance(appstruct.password, bytes)


def test_deserialize_errors():
    """
    Validate basic deserialization and verify that proper errors are raised
    """
    cstruct = dict(email='www.example.com', password='qwerty1234')
    with pytest.raises(colander.Invalid) as err:
        User.deserialize(cstruct)
    assert error_lookup('email', err, 'Invalid email address')
    assert error_lookup('name', err, 'Required')
    assert error_lookup('password', err, 'Invalid password token')
    assert len(err.value.children) == 3

