import csv
import datetime
from enum import Enum
from io import TextIOWrapper
import logging
import os
import sys
import zipfile

from cliquet.utils import msec_time
from pyramid_sqlalchemy import Session
from sqlalchemy import engine_from_config
import transaction
from repoze.lru import lru_cache

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from test_cliquet.model import Base, Continent, Country, City

logger = logging.getLogger('scripts.initialize')

PARENT_ID = 'basicauth:a43378bec53bb4f31b0294d8720f84db10dded2dc1571487167e7691981d521a'


class FILENAMES(Enum):

    countries = 'GeoLite2-Country-Locations-en.csv'
    cities = 'GeoLite2-City-Locations-en.csv'

continents = []
continent_name_id = {}


def accumulate_continents(value):
    """
    Pick continents from countries and populate a list of dictionaries with unique values

    :param value: country to inspect
    """
    if value[2] not in [i.code for i in continents]:
        continents.append(Continent(**{'code': value[2], 'name': value[3], 'sdate': datetime.datetime(2001, 1, 1),
                                       'parent_id': PARENT_ID, 'last_modified': msec_time()}))


def map_country_class(value):
    """
    Map a csv list to a dictionary useful to create a country instance

    :param value: a list of values
    :return: a dictionary where the input values has been mapped to keys
    """
    return {'locale': value[1], 'continent_id': value[2], 'code': value[4], 'name': value[5],
            'sdate': datetime.datetime(2001, 1, 1), 'parent_id': PARENT_ID, 'last_modified': msec_time()}


def map_city_class(value):
    """
    Map a csv list to a dictionary useful to create a city instance

    :param value: a list of values
    :return: a dictionary where the input values has been mapped to keys
    """
    return {'country_id': get_country_id(value[4]), 'sd_1_iso_code': value[6],
            'sd_1_name': value[7], 'sd_2_iso_code': value[8], 'sd_2_name': value[9],
            'name': value[10], 'metro_code': value[11], 'time_zone': value[12],
            'parent_id': PARENT_ID, 'last_modified': msec_time()}


@lru_cache(300)
def get_country_id(*args):
    """
    Query country database by code and return the corresponding integer id.

    :param args: code for lookup (passed as args due to caching mechanism)
    :return: tuple with id
    """
    return Session.query(Country.id).filter(Country.code == args[0]).one()[0]


def continent_conversion(list_of_continents):
    """
    Once continents have been flushed to db, update the continent_name_id dictionary with the equivalences between
    integer ids and continent codes

    :param list_of_continents: the populated dictionary of continents
    """
    for each in list_of_continents:
        continent_name_id[each.code] = each.id


def replace_continent_id(countries):
    """
    Iter all countries and translate the continent code to the proper continent integer id (as the continent list
    has been flushed to db and real ids exist)

    :param countries: list of instances of Country previous to be flushed to the db
    """
    for cnt, country in enumerate(countries):
        countries[cnt].continent_id = continent_name_id[country.continent_id]


def preload_countries():
    """
    Read the country list contained in GeoLite2.zip and populate the Continent and Country classes
    """
    countries = []
    cnt = 0
    with zipfile.ZipFile('test_cliquet/scripts/GeoLite2.zip') as zf:
        with TextIOWrapper(zf.open(FILENAMES.countries.value)) as data:
            reader = csv.reader(data)
            _ = next(reader)  # skip header
            for cnt, row in enumerate(reader):
                accumulate_continents(row)
                if row[5] != '':
                    countries.append(Country(**map_country_class(row)))
        logger.info('Loaded {} countries'.format(cnt))
        Session.add_all(continents)
        Session.flush()
        continent_conversion(continents)
        replace_continent_id(countries)
        Session.add_all(countries)


def preload_cities():
    """
    Read the city list contained in GeoLite2.zip and populate the City class
    """
    cnt = 0
    with zipfile.ZipFile('test_cliquet/scripts/GeoLite2.zip') as zf:
        with TextIOWrapper(zf.open(FILENAMES.cities.value)) as data:
            reader = csv.reader(data)
            _ = next(reader)  # skip header
            for row in reader:
                if row[10] != '':
                    Session.add(City(**map_city_class(row)))
        logger.info('Loaded {} cities'.format(cnt))


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    Session.configure(bind=engine)
    logger.info('Drop and create tables')
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        preload_countries()
        preload_cities()

if __name__ == '__main__':
    main()
