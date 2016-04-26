from database import *
from sqlalchemy import func, or_, literal
from geoalchemy2.shape import to_shape

def main():

    session = get_session()

    print "=="
    print "testing data"
    print "--"

    mpls = session.query(City).filter_by(ctu_name='Minneapolis').first()
    stp = session.query(City).filter_by(ctu_name='St. Paul').first()
    cities = [mpls, stp]

    msp_blockgroups = session.query(BlockGroup).filter(
        or_( func.ST_Within(BlockGroup.geom, mpls.geom)
           , func.ST_Within(BlockGroup.geom, stp.geom)
           )
    ).all()

    # If this fails then there's an issue with data being loaded or
    # something.
    assert len(msp_blockgroups) > 0

    blockgroups_with_stations = []
    stations = session.query(Station).all()

    # If this fails then there's an issue with datums
    assert len(session.query(Station).filter(func.ST_Within(Station.geom, mpls.geom)).all()) > 0

    for st in stations:
        sts = session.query(BlockGroup).filter(
            func.ST_Contains(BlockGroup.geom, st.geom)
        ).all()
        blockgroups_with_stations.append((tuple(sts), st))

    print "block groups:              %d" % len(session.query(BlockGroup).all())
    print "cities:                    %d" % len(session.query(City).all())
    print "stations:                  %d" % len(session.query(Station).all())
    print "stations in cities:        %d" % \
          (len(session.query(Station).filter(func.ST_Within(Station.geom, mpls.geom)).all()) + \
           len(session.query(Station).filter(func.ST_Within(Station.geom, stp.geom)).all()))

    print "blockgroups in mpls+stp:   %d" % len(msp_blockgroups)
    print "blockgroups with stations: %d" % len(list(set(blockgroups_with_stations)))
    print "--"
    print "Done. Stuff should be fine."
    print "=="


if __name__ == "__main__":
    main()
