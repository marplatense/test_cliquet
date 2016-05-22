from kinto.core.resource import register
from kinto.core.resource.sqlalchemy import SQLAUserResource

from test_cliquet import model


@register()
class Continent(SQLAUserResource):
    appmodel = model.Continent


@register(collection_path='/countries', record_path='/countries/{{id}}')
class Country(SQLAUserResource):
    appmodel = model.Country


@register(collection_path='/cities', record_path='/cities/{{id}}')
class City(SQLAUserResource):
    appmodel = model.Country
