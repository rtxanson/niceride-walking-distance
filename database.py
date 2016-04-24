from sqlalchemy import create_engine, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, column_property, object_session

from geoalchemy2 import Geometry

from settings import *

__all__ = [
    'get_session',
    'City',
    'BlockGroup',
    'HennStreet',
    'Bikeway',
    'RamseyStreet',
    'Station',
    'Ride',
    'BlockGroupProperties'
]

Base = declarative_base()

def get_session():
    engine = create_engine(DB_STRING)
    SessionMaker = sessionmaker(bind=engine)
    session = SessionMaker()
    return session

class Ride(Base):
    __tablename__ = "2013_rides"

    id = Column('gid', Integer, primary_key = True)

    duration = Column(String)
    start_date = Column(String)
    start_station = Column(String)
    start_terminal = Column(Integer)

    end_date = Column(String)
    end_station = Column(String)
    end_terminal = Column(Integer)

    bike_id = Column(String)

class Station(Base):
    __tablename__ = "bikestations"

    id            = Column('gid', Integer, primary_key = True)
    geom          = Column('geom', Geometry('POINT'))
    geojson = column_property(geom.ST_AsGeoJSON())

    terminal   = Column(Integer)
    address    = Column(String)

    def count_usage(self, session):
        starts = int(session.query(Ride).filter( Ride.start_terminal ==
                                         self.terminal) .count())
        ends   = int(session.query(Ride).filter( Ride.end_terminal ==
                                         self.terminal) .count())
        total  = starts + ends
        return (starts, ends, total)

class HennStreet(Base):
    __tablename__ = "location_hennepin_gis_street_centerline"

    id            = Column('gid', Integer, primary_key = True)
    geom          = Column('geom', Geometry('MULTILINESTRING'))
    geojson = column_property(geom.ST_AsGeoJSON())

    st_pre_mod = Column(String)
    st_pre_dir = Column(String)
    st_pre_typ = Column(String)
    st_name = Column(String)
    st_pos_typ = Column(String)
    st_pos_dir = Column(String)
    st_pos_mod = Column(String)
    street_cd = Column(Integer)
    street_nam = Column(String)
    lft_from = Column(Integer)
    lft_to = Column(Integer)
    rt_from = Column(Integer)
    rt_to = Column(Integer)
    lft_from2 = Column(Integer)
    lft_to2 = Column(Integer)
    rt_from2 = Column(Integer)
    rt_to2 = Column(Integer)
    lft_cad = Column(String)
    rt_cad = Column(String)
    lft_city = Column(String)
    rt_city = Column(String)
    lft_pcode = Column(Integer)
    rt_pcode = Column(Integer)
    lft_zip = Column(Integer)
    rt_zip = Column(Integer)
    alt_name1 = Column(String)
    alt_name2 = Column(String)
    join_id = Column(Integer)
    shape_leng = Column(Integer)

class RamseyStreet(Base):
    __tablename__ = "trans_street"

    id            = Column('gid', Integer, primary_key = True)
    geom          = Column('geom', Geometry('MULTILINESTRING'))
    geojson = column_property(geom.ST_AsGeoJSON())

    featureuni = Column('featureuni', String)
    routesyste = Column('routesyste', String)
    routeid = Column('routeid', String)
    streetprem = Column('streetprem', String)
    streetpred = Column('streetpred', String)
    streetpret = Column('streetpret', String)
    streetname = Column('streetname', String)
    streetpost = Column('streetpost', String)
    streetpo_1 = Column('streetpo_1', String)
    streetpo_2 = Column('streetpo_2', String)
    streetna_1 = Column('streetna_1', String)
    leftfromad = Column('leftfromad', Integer)
    rightfroma = Column('rightfroma', Integer)
    lefttoaddr = Column('lefttoaddr', Integer)
    righttoadd = Column('righttoadd', Integer)
    leftzip = Column('leftzip', String)
    rightzip = Column('rightzip', String)
    aliasname = Column('aliasname', String)
    leftpolice = Column('leftpolice', String)
    rightpolic = Column('rightpolic', String)
    leftfireid = Column('leftfireid', String)
    rightfirei = Column('rightfirei', String)
    leftemsid = Column('leftemsid', String)
    rightemsid = Column('rightemsid', String)
    leftcityid = Column('leftcityid', String)
    rightcityi = Column('rightcityi', String)
    leftcounty = Column('leftcounty', String)
    rightcount = Column('rightcount', String)
    leftstatei = Column('leftstatei', String)
    rightstate = Column('rightstate', String)
    featuretyp = Column('featuretyp', String)
    leftparity = Column('leftparity', String)
    rightparit = Column('rightparit', String)
    locationna = Column('locationna', String)
    routingstr = Column('routingstr', String)
    fromelevat = Column('fromelevat', Integer)
    toelevatio = Column('toelevatio', Integer)
    oneway = Column('oneway', String)
    impedences = Column('impedences', Integer)
    emergencya = Column('emergencya', String)
    routename = Column('routename', String)
    postedspee = Column('postedspee', Integer)
    layer = Column('layer', String)
    functional = Column('functional', String)
    snowplowro = Column('snowplowro', String)
    status = Column('status', String)
    editedby = Column('editedby', String)
    collection = Column('collection', String)
    altname1 = Column('altname1', String)
    altname2 = Column('altname2', String)
    leftcityna = Column('leftcityna', String)
    rightcityn = Column('rightcityn', String)

class Bikeway(Base):
    __tablename__ = "bikeways"

    id            = Column('gid', Integer, primary_key = True)
    geom          = Column('geom', Geometry('MULTILINESTRING'))
    geojson = column_property(geom.ST_AsGeoJSON())

    name = Column('name', String)
    type = Column('type', String)
    active = Column('active', Integer)

    lighted = Column('lighted', String)
    operation = Column('opperation', String)
    bikeway_class = Column('class', String)
    proposed = Column('proposed', String)
    road_name = Column('road_name', String)

# objectid integer,
# source character varying(20),
# side character varying(13),
# jurisdicti character varying(10),
# active integer,
# notes character varying(250),
# fac_id character varying(50),
# miles double precision,
# width integer,
# direction character varying(10),
# grade character varying(1),
# speed integer,
# fac_qual character varying(50),
# arterial character varying(1),
# conn_gap character varying(1),
# stops integer,
# road_numb character varying(10),
# road_code character varying(2),
# road_speed integer,
# road_comm character varying(1),
# lane_numb integer,
# lane_width integer,
# lane_dir character varying(10),
# lane_type character varying(24),
# shld_width double precision,
# shld_type character varying(50),
# shld_rumb character varying(1),
# shld_park character varying(24),
# shld_bus character varying(1),
# shape_leng numeric,
# maintainer character varying(35),
# install_yr character varying(16),
# install_or character varying(32),
# suitabilit character varying(24),
# shld_date date,
# shld_plow character varying(3),
# shld_drain character varying(3),
# road_aadt integer,
# road_hcadt character varying(1),
# surf_type character varying(25),
# surf_qaul character varying(25),

class City(Base):
    __tablename__ = 'census2010ctus'

    id            = Column('gid', Integer, primary_key = True)
    geom          = Column(Geometry('MULTIPOLYGON'))
    geojson = column_property(geom.ST_AsGeoJSON())

    ctu_name   = Column(String)
    ctu_id_cen = Column(String)
    ctu_code   = Column(String)
    ctu_type   = Column(String)
    ctu_id     = Column(Integer)
    abc_sort   = Column(Integer)
    five_color = Column(Integer)

    def __repr__(self):
        return "<City: %s>" % self.ctu_name



# BlockGroupProperties GEOG_UNIT and GEOID2 =  BlockGroup geoid10

class BlockGroupProperties(Base):

    __tablename__ = 'census2010tigerblockgroup_properties'

    id            = Column('id', Integer, primary_key = True)

    GEOG_UNIT    = Column(String)
    GEOG_LEVEL    = Column(String)
    GEONAME    = Column(String)
    GEOID    = Column(String)
    SUMLEV    = Column(String)
    GEOCOMP    = Column(String)
    STATE    = Column(String)
    COUNTY    = Column(String)
    GEOID2    = Column(String)
    B00001E1    = Column(Integer)
    B00002E1    = Column(Integer)
    POPTOTAL    = Column(Integer)
    LIVEDALONE    = Column(Integer)
    MARRKIDS    = Column(Integer)
    UNMARRKIDS    = Column(Integer)
    FAMNOKIDS    = Column(Integer)
    NONFAMILY    = Column(Integer)
    M_0_4    = Column(Integer)
    M_5_9    = Column(Integer)
    M_10_14    = Column(Integer)
    M_15_19    = Column(Integer)
    M_20_24    = Column(Integer)
    M_25_29    = Column(Integer)
    M_30_34    = Column(Integer)
    M_35_39    = Column(Integer)
    M_40_44    = Column(Integer)
    M_45_49    = Column(Integer)
    M_50_54    = Column(Integer)
    M_55_59    = Column(Integer)
    M_60_64    = Column(Integer)
    M_65_69    = Column(Integer)
    M_70_74    = Column(Integer)
    M_75_79    = Column(Integer)
    M_80_84    = Column(Integer)
    M_OVER85    = Column(Integer)
    F_0_4    = Column(Integer)
    F_5_9    = Column(Integer)
    F_10_14    = Column(Integer)
    F_15_19    = Column(Integer)
    F_20_24    = Column(Integer)
    F_25_29    = Column(Integer)
    F_30_34    = Column(Integer)
    F_35_39    = Column(Integer)
    F_40_44    = Column(Integer)
    F_45_49    = Column(Integer)
    F_50_54    = Column(Integer)
    F_55_59    = Column(Integer)
    F_60_64    = Column(Integer)
    F_65_69    = Column(Integer)
    F_70_74    = Column(Integer)
    F_75_79    = Column(Integer)
    F_80_84    = Column(Integer)
    F_OVER85    = Column(Integer)
    AGEUNDER18    = Column(Integer)
    AGE18_39    = Column(Integer)
    AGE40_64    = Column(Integer)
    AGE65UP    = Column(Integer)
    WHITENH    = Column(Integer)
    BLACKNH    = Column(Integer)
    AMINDNH    = Column(Integer)
    ASIANNH    = Column(Integer)
    PACIFICNH    = Column(Integer)
    OTHERNH    = Column(Integer)
    MULTRACENH    = Column(Integer)
    HISPPOP    = Column(Integer)
    NOTHISPPOP    = Column(Integer)
    HUTOTAL    = Column(Integer)
    HHTOTAL    = Column(Integer)
    POPINHH    = Column(Integer)
    AVGHHSIZE    = Column(Float)
    POPINGQ    = Column(Integer)
    HOMEOWNPCT    = Column(Float)
    OWNEROCC    = Column(Integer)
    RENTEROCC    = Column(Integer)
    VACANT    = Column(Integer)
    POPOVER5    = Column(Integer)
    POPOVER16    = Column(Integer)
    POPOVER18    = Column(Integer)
    POPOVER65    = Column(Integer)
    MEDIANAGE    = Column(Float)
    HH_UNDER18    = Column(Integer)
    HH_65OVER    = Column(Integer)
    ERRORFLAG    = Column(Integer)
    SOURCE    = Column(String)
    YEAR    = Column(String)
    TCFLAG    = Column(String)

# STATEFP10, 2, String, 2010 Census state FIPS code 
# COUNTYFP10, 3, String, 2010 Census county FIPS code 
# TRACTCE10, 6, String, 2010 Census census tract code 
# BLOCKCE10, 4, String, 2010 Census tabulation block number 
# GEOID10, 15, String, Block identifier; a concatenation of 2010 Census state FIPS code, county FIPS code, census tract code and tabulation block number. 
# NAME10, 10, String, 2010 Census tabulation block name; a concatenation of 'Block' and the current tabulation block number 
# MTFCC10, 5, String, MAF/TIGER feature class code (G5040) 
# UR10, 1, String, 2010 Census urban/rural indicator 
# UACE10, 5, String, 2010 Census urban area code 
# FUNCSTAT10, 1, String, 2010 Census functional status 
# ALAND10, 14, Number, 2010 Census land area (square meters) 
# AWATER10, 14, Number, 2010 Census water area (square meters) 
# INTPTLAT10, 11, String, 2010 Census latitude of the internal point 
# INTPTLON10, 12, String, 2010 Census longitude of the internal point 

class BlockGroup(Base):
    __tablename__ = 'census2010tigerblockgroup'

    id            = Column('gid', Integer, primary_key = True)
    namelsad10    = Column(String)
    geom          = Column(Geometry('MULTIPOLYGON'))

    statefp10  = Column(String)
    countyfp10 = Column(String)
    tractce10  = Column(String)
    blkgrpce10 = Column(String)
    geoid10    = Column(String)
    mtfcc10    = Column(String)
    funcstat10 = Column(String)
    aland10    = Column(Float)
    awater10   = Column(Float)
    intptlat10 = Column(String)
    intptlon10 = Column(String)
    shape_area = Column(Float)
    shape_len  = Column(Float)

    geojson = column_property(geom.ST_AsGeoJSON())

    def __repr__(self):
        return "<BlockGroup: %s, %s>" % (self.geoid10, self.namelsad10)

    def get_properties(self, session):
        return session.query(BlockGroupProperties).filter(
            BlockGroupProperties.GEOID2 == self.geoid10
        ).all()

    @property
    def DENSITY(self):
        props = self.get_properties(object_session(self))[0]
        area = self.shape_area
        pop = props.POPTOTAL
        return float(pop)/float(area)

