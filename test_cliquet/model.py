from kinto.core.resource.sqlalchemy import Base
from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, DateTime, Boolean, Integer
from sqlalchemy.orm import relationship


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
