from database import *
from sqlalchemy import func, or_, literal, not_
from geoalchemy2.shape import to_shape
import sys

from numpy import average as avg

def colate_demos(session, groups):
    group_props = sum([g.get_properties(session) for g in groups], [])
    _whiteness = [float(bgp.WHITENH)/float(bgp.POPTOTAL) for bgp in group_props]
    _blackness = [float(bgp.BLACKNH)/float(bgp.POPTOTAL) for bgp in group_props]
    _avg_pop = avg([float(bgp.POPTOTAL) for bgp in group_props])
    _tot_pop = sum([float(bgp.POPTOTAL) for bgp in group_props])
    return (avg(_whiteness), avg(_blackness), _avg_pop, _tot_pop)

def calc_for_region(session, reg):
    bgs = session.query(BlockGroup).filter(
        func.ST_Within(BlockGroup.geom, reg.geom)
    )
    print "total blockgroups in region: %d" % len(bgs.all())
    bgps = sum([bg.get_properties(session) for bg in bgs], [])

    # blockgroups_with_stations = []
    # stations = session.query(Station).all()
    # for st in stations:
    #     sts = session.query(BlockGroup).filter(
    #         func.ST_Contains(BlockGroup.geom, st.geom)
    #     ).all()
    #     blockgroups_with_stations.extend(sts)

    blockgroups_with_stations = session.query(BlockGroup)\
        .filter(
            func.ST_Within(BlockGroup.geom, reg.geom)
        )\
        .filter(
            func.ST_Contains(BlockGroup.geom, Station.geom)
        ).all()

    bgstation_ids = [bg.id for bg in blockgroups_with_stations]

    blockgroups_without_stations = session.query(BlockGroup)\
        .filter(
            func.ST_Within(BlockGroup.geom, reg.geom)
        )\
        .filter(
            not_(BlockGroup.id.in_(bgstation_ids))
        ).all()

    from collections import defaultdict

    blockgroups_by_station_amt = defaultdict(list)

    for bg in blockgroups_with_stations:
        bg_stations = session.query(Station).filter(
            func.ST_Contains(bg.geom, Station.geom)
        ).all()
        blockgroups_by_station_amt[len(bg_stations)].append(bg)

    print "block groups with stations: %d" % len(blockgroups_with_stations)
    print "block groups without stations: %d" % len(blockgroups_without_stations)

    print "calculating whiteness/blackness averages for all block groups in region..."

    avg_whiteness = [float(bgp.WHITENH)/float(bgp.POPTOTAL) for bgp in bgps]
    print "avg % white: " + str(avg(avg_whiteness))

    avg_blackness = [float(bgp.BLACKNH)/float(bgp.POPTOTAL) for bgp in bgps]
    print "avg % black: " + str(avg(avg_blackness))

    stats_with = colate_demos(session, blockgroups_with_stations)
    stats_without = colate_demos(session, blockgroups_without_stations)

    print "calculating whiteness/blackness averages for block groups with stations..."
    avg_whiteness, avg_blackness, _avg_pop, _tot_pop = stats_with

    print "avg % white: " + str(avg(avg_whiteness))
    print "avg % black: " + str(avg(avg_blackness))
    print "avg pop:     " + str(_avg_pop)
    print "tot pop:     " + str(_tot_pop)

    print "calculating whiteness/blackness averages for block groups WITHOUT stations..."
    avg_whiteness_wo, avg_blackness_wo, _avg_pop_wo, _tot_pop_wo = stats_without
    print "avg % white: " + str(avg(avg_whiteness_wo))
    print "avg % black: " + str(avg(avg_blackness_wo))
    print "avg pop:     " + str(_avg_pop_wo)
    print "tot pop:     " + str(_tot_pop_wo)

    print "Block groups with x amount of stations: "
    for k, v in blockgroups_by_station_amt.iteritems():
        print "  %s blockgroups with %s stations" % (len(v), k)
        avg_w, avg_b, avg_p, tot_p = colate_demos(session, v)
        print "    avg white: " + str(avg_w)
        print "    avg black: " + str(avg_b)
        print "    avg pop: "   + str(avg_p)
        print "    cumulative pop: " + str(tot_p)

def nice_ride_total(session):
    station = session.query(Station).all()

    for s in station:
        print (s.address, s.count_usage(session))

def main():

    session = get_session()

    mpls = session.query(City).filter_by(ctu_name='Minneapolis').first()
    stp = session.query(City).filter_by(ctu_name='St. Paul').first()

    print '--'
    print 'MINNEAPOLIS'
    calc_for_region(session, mpls)
    print '--'
    print '--'
    print 'SAINT PAUL'
    calc_for_region(session, stp)
    print '--'
    print '--'


    sys.exit()


    # print len(bgs)
    # print len(list(set([bg.geoid10 for bg in bgs])))
    # print list(set([bg.geoid10 for bg in bgs]))[0:10]


    # print emit_featurecollection(bgs)


    # TRY:
    # average block group WHITENH and BLACKNH for all block groups
    # average block group WHITENH and BLACKNH for all block groups
    # containing niceride stations



if __name__ == "__main__":
    main()
