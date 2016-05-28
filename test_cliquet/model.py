import base64
import colander
from colanderalchemy import SQLAlchemySchemaNode
from kinto.core.resource.sqlalchemy import Base
from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, DateTime, Boolean, Integer
from sqlalchemy.orm import relationship

key = SQLAlchemySchemaNode.sqla_info_key


class User(Base):
    __tablename__ = "users"
    name = Column(String, nullable=False, info={key: {'repr': True}})
    email = Column(String, nullable=False, unique=True, info={key: {'validator': colander.Email(), 'repr': True}})
    password = Column(String, nullable=False)

    @staticmethod
    def password_preparer(value):
        return value + ':000'

    @staticmethod
    def password_validator(node, value):
        if not value.startswith('abc:'):
            raise colander.Invalid(node, msg='Invalid password token', value=value)
        return True

    @staticmethod
    def global_preparer(value):
        value['password'] = base64.b64encode(value['password'].encode('ascii'))
        return value

    @staticmethod
    def global_validator(*args):
        pass


class Continent(Base):
    __tablename__ = "continents"
    code = Column(String(2), nullable=False, index=True, unique=True)
    name = Column(String(), nullable=False, index=True)
    sdate = Column(DateTime)
    valid = Column(Boolean, default=True, index=True)


class Country(Base):
    __tablename__ = "countries"
    code = Column(String(), nullable=False, unique=True)
    name = Column(String(), nullable=False)
    continent_id = Column(Integer, ForeignKey('continents.id'), index=True, nullable=False)
    locale = Column(String(2), nullable=False, index=True)
    sdate = Column(DateTime)
    valid = Column(Boolean, default=True, index=True)

    continent = relationship(Continent, backref='countries')


class City(Base):
    __tablename__ = "cities"
    sd_1_iso_code = Column(String())
    sd_1_name = Column(String())
    sd_2_iso_code = Column(String())
    sd_2_name = Column(String())
    name = Column(String(), nullable=False)
    metro_code = Column(String())
    time_zone = Column(String(), nullable=False)
    country_id = Column(Integer, ForeignKey('countries.id'), index=True, nullable=False)
    sdate = Column(DateTime)
    valid = Column(Boolean, default=True, index=True)

    #country = relationship(Country, backref='cities')
