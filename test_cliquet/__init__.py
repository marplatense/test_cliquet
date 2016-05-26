import datetime
import logging

from pyramid.config import Configurator
from pyramid.renderers import JSON

from kinto.core import initialization, install_middlewares

logger = logging.getLogger(__name__)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_sqlalchemy')
    json_renderer = JSON()

    def datetime_adapter(obj, request):
        return obj.isoformat()

    json_renderer.add_adapter(datetime.datetime, datetime_adapter)
    config.add_renderer('json', json_renderer)
    initialization.initialize(config)

    config.scan()
    app = config.make_wsgi_app()
    return install_middlewares(app, settings)
