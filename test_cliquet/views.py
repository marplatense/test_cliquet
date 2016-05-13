import cliquet.resource
from cliquet.resource.sqlalchemy import SQLAUserResource

from test_cliquet import model


@cliquet.resource.register()
class Continent(SQLAUserResource):
    appmodel = model.Continent


@cliquet.resource.register(collection_path='/countries', record_path='/countries/{{id}}')
class Country(SQLAUserResource):
    appmodel = model.Country


@cliquet.resource.register(collection_path='/cities', record_path='/cities/{{id}}')
class City(SQLAUserResource):
    appmodel = model.Country
