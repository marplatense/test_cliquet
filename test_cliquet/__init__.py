import datetime
import logging

from pyramid.config import Configurator
from pyramid.renderers import JSON

import cliquet

logger = logging.getLogger(__name__)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    json_renderer = JSON()

    def datetime_adapter(obj, request):
        return obj.isoformat()

    json_renderer.add_adapter(datetime.datetime, datetime_adapter)
    config.add_renderer('json', json_renderer)
    cliquet.initialize(config)

    config.scan()
    app = config.make_wsgi_app()
    return cliquet.install_middlewares(app, settings)
