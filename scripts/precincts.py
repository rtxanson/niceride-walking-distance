from database import *
from sqlalchemy import func, or_, literal
from geoalchemy2.shape import to_shape

def main():

    session = get_session()

    print "=="
    print "testing data"
    print "--"

    prec = session.query(Precinct).filter_by(pctname='Minneapolis W-9 P-6').first()

    props = session.query(Prop).filter(func.ST_Within(Prop.geom, prec.geom)).all()

    print "(" + ', '.join([p.pid for p in props]) + ')'

    print "=="
    print len(props)


if __name__ == "__main__":
    main()

