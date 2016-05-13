import csv
import zipfile

import cliquet
from cliquet import DEFAULT_SETTINGS
from cliquet.tests.support import get_request_class
from pyramid.config import Configurator
import pytest
import webtest

from test_cliquet.model import Continent, Country, City

USER_PRINCIPAL = ('basicauth:9f2d363f98418b13253d6d7193fc88690302'
                  'ab0ae21295521f6029dffe9dc3b0')
api_prefix = "v0"
authorization_policy = 'cliquet.tests.support.AllowAuthorizationPolicy'
collection_url = '/mushrooms'
principal = USER_PRINCIPAL


def testapp(settings=None, config=None, *args, **additional_settings):
    if settings is None:
        settings = {}
    settings.update(additional_settings)
    if config is None:
        config = Configurator(settings=settings)
    cliquet.initialize(config, version='0.0.1')
    config.scan("test_cliquet.views")
    app = config.make_wsgi_app()
    # Install middleware (no-op if not enabled in setting)
    return cliquet.install_middlewares(app, settings)


def get_app_settings(additional_settings=None):
    settings = DEFAULT_SETTINGS.copy()

    settings['storage_backend'] = 'cliquet.storage.sqlalchemy'
    settings['sqlalchemy.url'] = 'postgres://mariano:otroletravaladna@localhost:5432/cliquet_test'
    settings['cache_backend'] = 'cliquet.cache.redis'
    settings['permission_backend'] = 'cliquet.permission.postgresql'
    settings['permission_url'] = 'postgres://mariano:otroletravaladna@localhost:5432/cliquet_test'

    settings['project_name'] = 'myapp'
    settings['project_version'] = '0.0.1'
    settings['project_docs'] = 'https://cliquet.rtfd.org/'
    settings['multiauth.authorization_policy'] = authorization_policy

    if additional_settings is not None:
        settings.update(additional_settings)
    return settings


@pytest.fixture(scope="session")
def app():
    wsgi_app = testapp(get_app_settings())
    app = webtest.TestApp(wsgi_app)
    app.RequestClass = get_request_class(api_prefix)
    return app


@pytest.fixture
def load_country_data(sql_session):
    filenames = ('GeoLite2-Country-Locations-en.csv', 'GeoLite2-City-Locations-en.csv')
    with zipfile.ZipFile('tests/databases/GeoLite2.zip') as zf:
        for filename in filenames:
            with zf.open(filename) as data:
                reader = csv.reader(data)
                header = next(reader)
                for row in reader:
                    pass

