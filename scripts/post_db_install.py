from database import *
from sqlalchemy import func, or_, literal, not_
from geoalchemy2.shape import to_shape
import sys

def trim_data(session):
    mpls = session.query(City).filter_by(ctu_name='Minneapolis').first()
    stp = session.query(City).filter_by(ctu_name='St. Paul').first()
    cities = [mpls, stp]

    not_msp_blockgroups = session.query(BlockGroup).filter(
        not_(or_( func.ST_Within(BlockGroup.geom, mpls.geom)
                , func.ST_Within(BlockGroup.geom, stp.geom)
                , func.ST_Intersects(BlockGroup.geom, mpls.geom)
                , func.ST_Intersects(BlockGroup.geom, stp.geom)
                )
            )
    ).all()

    print " * Deleting block groups outside of cities."
    print len(session.query(BlockGroup).all()) -  len(not_msp_blockgroups)
    print len(
        session.query(BlockGroup).filter(
            or_( func.ST_Within(BlockGroup.geom, mpls.geom)
               , func.ST_Within(BlockGroup.geom, stp.geom)
               )
        ).all()
    )
    not_msp_blockgroups = session.query(BlockGroup).filter(
        not_(or_( func.ST_Within(BlockGroup.geom, mpls.geom)
                , func.ST_Within(BlockGroup.geom, stp.geom)
                )
            )
    )
    not_msp_blockgroups.delete(synchronize_session='fetch')
    session.commit()
    print " * Done."

def read_csv(session, model, filename):
    import csv

    header_column_type = {
        'GEOG_UNIT'  : [str],
        'GEOG_LEVEL' : [str],
        'GEONAME'    : [str],
        'GEOID'      : [str],
        'SUMLEV'     : [str],
        'GEOCOMP'    : [str],
        'STATE'      : [str],
        'COUNTY'     : [str],
        'GEOID2'     : [str],
        'B00001E1'   : [int],
        'B00002E1'   : [int],
        'POPTOTAL'   : [int],
        'LIVEDALONE' : [int],
        'MARRKIDS'   : [int],
        'UNMARRKIDS' : [int],
        'FAMNOKIDS'  : [int],
        'NONFAMILY'  : [int],
        'M_0_4'      : [int],
        'M_5_9'      : [int],
        'M_10_14'    : [int],
        'M_15_19'    : [int],
        'M_20_24'    : [int],
        'M_25_29'    : [int],
        'M_30_34'    : [int],
        'M_35_39'    : [int],
        'M_40_44'    : [int],
        'M_45_49'    : [int],
        'M_50_54'    : [int],
        'M_55_59'    : [int],
        'M_60_64'    : [int],
        'M_65_69'    : [int],
        'M_70_74'    : [int],
        'M_75_79'    : [int],
        'M_80_84'    : [int],
        'M_OVER85'   : [int],
        'F_0_4'      : [int],
        'F_5_9'      : [int],
        'F_10_14'    : [int],
        'F_15_19'    : [int],
        'F_20_24'    : [int],
        'F_25_29'    : [int],
        'F_30_34'    : [int],
        'F_35_39'    : [int],
        'F_40_44'    : [int],
        'F_45_49'    : [int],
        'F_50_54'    : [int],
        'F_55_59'    : [int],
        'F_60_64'    : [int],
        'F_65_69'    : [int],
        'F_70_74'    : [int],
        'F_75_79'    : [int],
        'F_80_84'    : [int],
        'F_OVER85'   : [int],
        'AGEUNDER18' : [int],
        'AGE18_39'   : [int],
        'AGE40_64'   : [int],
        'AGE65UP'    : [int],
        'WHITENH'    : [int],
        'BLACKNH'    : [int],
        'AMINDNH'    : [int],
        'ASIANNH'    : [int],
        'PACIFICNH'  : [int],
        'OTHERNH'    : [int],
        'MULTRACENH' : [int],
        'HISPPOP'    : [int],
        'NOTHISPPOP' : [int],
        'HUTOTAL'    : [int],
        'HHTOTAL'    : [int],
        'POPINHH'    : [int],
        'AVGHHSIZE'  : [float],
        'POPINGQ'    : [int],
        'HOMEOWNPCT' : [float],
        'OWNEROCC'   : [int],
        'RENTEROCC'  : [int],
        'VACANT'     : [int],
        'POPOVER5'   : [int],
        'POPOVER16'  : [int],
        'POPOVER18'  : [int],
        'POPOVER65'  : [int],
        'MEDIANAGE'  : [float],
        'HH_UNDER18' : [int],
        'HH_65OVER'  : [int],
        'ERRORFLAG'  : [int],
        'SOURCE'     : [str],
        'YEAR'       : [str],
        'TCFLAG'     : [str],
    }

    def get_kwargs(d):
        kwargs = {}
        for k, v in d.iteritems():
            _type = header_column_type.get(k, str)[0]
            try:
                kwargs[k] = _type(v)
            except Exception, e:
                print e
                print k, v
                sys.exit()

        return kwargs

    def create_obj(kw):
        return model(**kw)

    with open(filename, 'r') as F:
        reader = csv.DictReader(F)

        objs = map(create_obj, map(get_kwargs, reader))

    print 'Adding %d objects' % len(objs)

    session.add_all(objs)
    session.commit()

    print 'Added %d instances of %s' % (len(objs), repr(model))

def read_ride_csv(session, model, filename):

    import csv

    csv_to_column = {
        'Duration': 'duration',
        'Start date': 'start_date',
        'Start Station': 'start_station',
        'Start terminal': 'start_terminal',
        'End date': 'end_date',
        'End Station': 'end_station',
        'End terminal': 'end_terminal',
        'Bike#': 'bike_id',
    }

    header_column_type = {
        'duration': [str],
        'start_date': [str],
        'start_station': [str],
        'start_terminal': [int],
        'end_date': [str],
        'end_station': [str],
        'end_terminal': [int],
        'bike_id': [str],
    }

    def get_kwargs(d):
        kwargs = {}
        for k, v in d.iteritems():
            _r_k = csv_to_column.get(k)
            _type = header_column_type.get(_r_k, str)[0]
            try:
                kwargs[_r_k] = _type(v)
            except ValueError:
                if isinstance(v, str):
                    if v.strip() == None:
                        continue
            except Exception, e:
                print type(e)
                print e
                print _r_k, k, repr(v), _type
                sys.exit()

        return kwargs

    def create_obj(kw):
        return model(**kw)

    print 'Reading %s' % filename

    with open(filename, 'r') as F:
        reader = csv.DictReader(F)

        objs = map(create_obj, map(get_kwargs, reader))

    print 'Adding %d objects' % len(objs)

    session.add_all(objs)
    session.commit()

    print 'Added %d instances of %s' % (len(objs), repr(model))

def init_new_tables(session):
    from sqlalchemy import create_engine
    engine = create_engine('postgresql://pyry@localhost/walking')

    try:
        BlockGroupProperties.__table__.drop(engine)
    except:
        print "<BlockGroupProperties> Didn't exist, could not drop"
    print BlockGroupProperties.__table__.create(engine)
    print session.query(BlockGroupProperties).all()

    try:
        Ride.__table__.drop(engine)
    except:
        print "<Ride> Didn't exist, could not drop"
    print Ride.__table__.create(engine)
    print session.query(Ride).all()

def main():

    print "Beginning CSV install."
    session = get_session()

    init_new_tables(session)
    # read_csv(session, BlockGroupProperties, 'data/blockgroup_population.csv')
    # read_ride_csv(session, Ride, 'data_src/NRMN-2013-results/all-rentals-2013.csv')

    print "Cleaning data."
    # trim_data(session)

    print "Done."

if __name__ == "__main__":
    main()

