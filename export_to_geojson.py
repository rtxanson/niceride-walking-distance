import sys
from database import *
from sqlalchemy import func, or_, literal, and_

import simplejson as _json

def emit_bikeways_featurecollection(session, objs):

    from vectorformats.Feature import Feature
    import vectorformats.Formats.GeoJSON

    g = vectorformats.Formats.GeoJSON.GeoJSON(crs={
        'properties': {
            'name': 'urn:ogc:def:crs:OGC:1.3:CRS84'
        }
    })

    def get_attrs(o):
        json = {}
        for col in o._sa_class_manager.mapper.mapped_table.columns:
            json[col.name] = getattr(o, col.name)
        return json

    features = []
    for obj in objs:
        o_name = obj.name
        if o_name is None:
            o_name = obj.road_name
        obj_properties = {
            'name': obj.name,
            'path_type': obj.type,
            'bikeway_class': obj.bikeway_class,
            'operation': obj.operation,
            'lighted': obj.lighted,
        }
        feature = Feature(
            id=obj.id,
            geometry=_json.loads(obj.geojson),
            props=obj_properties
        )
        features.append(feature)

    return g.encode(features)


def emit_streets_featurecollection(session, msp_objs, stp_objs):

    from vectorformats.Feature import Feature
    import vectorformats.Formats.GeoJSON

    g = vectorformats.Formats.GeoJSON.GeoJSON(crs={
        'properties': {
            'name': 'urn:ogc:def:crs:OGC:1.3:CRS84'
        }
    })

    def get_attrs(o):
        json = {}
        for col in o._sa_class_manager.mapper.mapped_table.columns:
            json[col.name] = getattr(o, col.name)
        return json

    features = []
    for obj in msp_objs:
        obj_properties = {
            'name': obj.street_nam,
            'street_type': obj.st_pre_typ
        }
        feature = Feature(
            id=obj.id,
            geometry=_json.loads(obj.geojson),
            props=obj_properties
        )
        features.append(feature)

    for obj in stp_objs:
        obj_properties = {
            'name': obj.streetna_1,
            'street_type': obj.streetpret
        }
        feature = Feature(
            id=obj.id,
            geometry=_json.loads(obj.geojson),
            props=obj_properties
        )
        features.append(feature)

    return g.encode(features)

def emit_station_featurecollection(session, objs):

    from vectorformats.Feature import Feature
    import vectorformats.Formats.GeoJSON

    g = vectorformats.Formats.GeoJSON.GeoJSON(crs={
        'properties': {
            'name': 'urn:ogc:def:crs:OGC:1.3:CRS84'
        }
    })

    def get_attrs(o):
        json = {}
        for col in o._sa_class_manager.mapper.mapped_table.columns:
            json[col.name] = getattr(o, col.name)
        return json

    features = []
    for obj in objs:
        _start, _end, _total = obj.count_usage(session)
        obj_properties = {
            'uses': _total,
            'uses_departing': _start,
            'uses_arriving': _end,
            'address': obj.address,
            'name': obj.terminal,
            'id': obj.id,
        }
        feature = Feature(
            id=obj.id,
            geometry=_json.loads(obj.geojson),
            props=obj_properties
        )
        features.append(feature)

    return g.encode(features)

def emit_city_featurecollection(session, objs):

    from vectorformats.Feature import Feature
    import vectorformats.Formats.GeoJSON

    g = vectorformats.Formats.GeoJSON.GeoJSON(crs={
        'properties': {
            'name': 'urn:ogc:def:crs:OGC:1.3:CRS84'
        }
    })

    def get_attrs(o):
        json = {}
        for col in o._sa_class_manager.mapper.mapped_table.columns:
            json[col.name] = getattr(o, col.name)
        return json

    features = []
    for obj in objs:
        obj_properties = {}
        feature = Feature(
            id=obj.id,
            geometry=_json.loads(obj.geojson),
            props=obj_properties
        )
        features.append(feature)

    return g.encode(features)

def emit_blockgroup_featurecollection(session, objs):

    from vectorformats.Feature import Feature
    import vectorformats.Formats.GeoJSON

    g = vectorformats.Formats.GeoJSON.GeoJSON(crs={
        'properties': {
            'name': 'urn:ogc:def:crs:OGC:1.3:CRS84'
        }
    })

    def get_attrs(o):
        json = {}
        for col in o._sa_class_manager.mapper.mapped_table.columns:
            json[col.name] = getattr(o, col.name)
        return json

    features = []
    for obj in objs:
        ps = obj.get_properties(session)
        if len(ps) > 0:
            props = ps[0]
        obj_properties = get_attrs(props)
        obj_properties['DENSITY'] = obj.DENSITY
        obj_properties['AREA'] = obj.shape_area
        feature = Feature(
            id=obj.id,
            geometry=_json.loads(obj.geojson),
            props=obj_properties
        )
        features.append(feature)

    return g.encode(features)

model_names = {
    'blockgroup': BlockGroup,
    'station': Station,
    'city': City,
    'streets': HennStreet,
    'bikeways': Bikeway,
}

allowed_streets = [
    'WASHBURN AVENUE NORTH',
    'BROADWAY STREET NORTHEAST',
    'FRANKLIN AVENUE EAST',
    'FRANKLIN AVENUE WEST',
    'LAKE STREET EAST',
    'LAKE STREET WEST',

    'Snelling Avenue North',
    'Snelling Avenue South',
    'Lexington Avenue North',
    'Lexington Avenue South',
    'Lexington Parkway North',
    'Lexington Parkway South',

    'University Avenue East',
    'University Avenue West',

    'Larpenteur Avenue East',
    'Larpenteur Avenue West',

    'Hamline Avenue North',
    'Hamline Avenue South',

    'Minnehaha Avenue East',

    'Arcade Street',

    'Como Avenue',

    'Grand Avenue',

    'Ford Parkway',

    'Summit Avenue',

    'Dale Street North',
    'Dale Street South',
]

allowed_alt_names = [
    "COUNTY ROAD 1",
    "COUNTY ROAD 10",
    "COUNTY ROAD 101",
    "COUNTY ROAD 101  SOUTH",
    "COUNTY ROAD 102",
    "COUNTY ROAD 103",
    "COUNTY ROAD 109",
    "COUNTY ROAD 110  NORTH",
    "COUNTY ROAD 110  WEST",
    "COUNTY ROAD 115",
    "COUNTY ROAD 116",
    "COUNTY ROAD 117",
    "COUNTY ROAD 118",
    "COUNTY ROAD 12",
    "COUNTY ROAD 121",
    "COUNTY ROAD 122",
    "COUNTY ROAD 123",
    "COUNTY ROAD 125",
    "COUNTY ROAD 13",
    "COUNTY ROAD 130",
    "COUNTY ROAD 135",
    "COUNTY ROAD 136",
    "COUNTY ROAD 139",
    "COUNTY ROAD 14",
    "COUNTY ROAD 144",
    "COUNTY ROAD 146",
    "COUNTY ROAD 15",
    "COUNTY ROAD 150",
    "COUNTY ROAD 151",
    "COUNTY ROAD 152",
    "COUNTY ROAD 153",
    "COUNTY ROAD 156",
    "COUNTY ROAD 158",
    "COUNTY ROAD 159",
    "COUNTY ROAD 16",
    "COUNTY ROAD 16  EAST",
    "COUNTY ROAD 17",
    "COUNTY ROAD 19",
    "COUNTY ROAD 2",
    "COUNTY ROAD 20",
    "COUNTY ROAD 201",
    "COUNTY ROAD 202",
    "COUNTY ROAD 203",
    "COUNTY ROAD 204",
    "COUNTY ROAD 205",
    "COUNTY ROAD 21",
    "COUNTY ROAD 22",
    "COUNTY ROAD 23",
    "COUNTY ROAD 25",
    "COUNTY ROAD 27",
    "COUNTY ROAD 28",
    "COUNTY ROAD 29",
    "COUNTY ROAD 3",
    "COUNTY ROAD 30",
    "COUNTY ROAD 31",
    "COUNTY ROAD 32",
    "COUNTY ROAD 33",
    "COUNTY ROAD 34",
    "COUNTY ROAD 35",
    "COUNTY ROAD 36",
    "COUNTY ROAD 37",
    "COUNTY ROAD 39",
    "COUNTY ROAD 4",
    "COUNTY ROAD 40",
    "COUNTY ROAD 42",
    "COUNTY ROAD 43",
    "COUNTY ROAD 44",
    "COUNTY ROAD 46",
    "COUNTY ROAD 48",
    "COUNTY ROAD 5",
    "COUNTY ROAD 50",
    "COUNTY ROAD 51",
    "COUNTY ROAD 52",
    "COUNTY ROAD 53",
    "COUNTY ROAD 57",
    "COUNTY ROAD 6",
    "COUNTY ROAD 60",
    "COUNTY ROAD 61",
    "COUNTY ROAD 62",
    "COUNTY ROAD 66",
    "COUNTY ROAD 70",
    "COUNTY ROAD 73",
    "COUNTY ROAD 8",
    "COUNTY ROAD 81",
    "COUNTY ROAD 82",
    "COUNTY ROAD 83",
    "COUNTY ROAD 84",
    "COUNTY ROAD 88",
    "COUNTY ROAD 9",
    "COUNTY ROAD 92",
    "COUNTY ROAD 93",
    "COUNTY ROAD 94",

    # Ramsey county, ex.: Clifton Drive
]

allowed_street_types = [
    'INTERSTATE',
    'HIGHWAY',
    'UNITED STATES HIGHWAY',
    'COUNTY ROAD',
    'STATE HIGHWAY',

    # Ramsey
    'Highway',
    'Interstate',
    'County Road'
]

def main():
    model_name = sys.argv[1]

    try:
        outfile = sys.argv[2]
    except:
        outfile = 'stdout'

    model_name = model_name.lower()

    model = model_names.get(model_name, False)

    if not model:
        print >> sys.stderr, "No model matched."
        sys.exit()

    session = get_session()

    mpls = session.query(City).filter_by(ctu_name='Minneapolis').first()
    stp = session.query(City).filter_by(ctu_name='St. Paul').first()
    cities = [mpls, stp]

    stations = session.query(Station).all()

    msp_streets = session.query(HennStreet).filter(
        and_(
            or_( HennStreet.lft_city == 'MINNEAPOLIS'
               , HennStreet.rt_city == 'MINNEAPOLIS'
               )
          , or_( HennStreet.street_nam.in_(allowed_streets)
               , HennStreet.st_pre_typ.in_(allowed_street_types)
               , HennStreet.alt_name1.in_(allowed_alt_names)
               )
        )
    )

    stp_streets = session.query(RamseyStreet).filter(
        and_(
            or_( RamseyStreet.leftcityna == 'Saint Paul'
               , RamseyStreet.rightcityn == 'Saint Paul'
               )
          , or_( RamseyStreet.streetna_1.in_(allowed_streets)
               , RamseyStreet.streetpret.in_(allowed_street_types)
               , RamseyStreet.altname1.in_(allowed_alt_names)
               )
        )
    )

    if model_name == 'blockgroup':

        msp_blockgroups = session.query(BlockGroup).filter(
            or_( func.ST_Within(BlockGroup.geom, mpls.geom)
               , func.ST_Within(BlockGroup.geom, stp.geom)
               , func.ST_Intersects(BlockGroup.geom, mpls.geom)
               , func.ST_Intersects(BlockGroup.geom, stp.geom)
               )
        ).all()

        output_json = emit_blockgroup_featurecollection(session, msp_blockgroups)
    elif model_name == 'city':
        output_json = emit_city_featurecollection(session, cities)
    elif model_name == 'station':
        output_json = emit_station_featurecollection(session, stations)
    elif model_name == 'streets':
        output_json = emit_streets_featurecollection(session, msp_streets, stp_streets)
    elif model_name == 'bikeways':

        bikeways = session.query(Bikeway)\
            .filter(
                    or_( func.ST_Intersects(Bikeway.geom, mpls.geom)
                       , func.ST_Intersects(Bikeway.geom, stp.geom)
                       , func.ST_Within(Bikeway.geom, stp.geom)
                       , func.ST_Within(Bikeway.geom, mpls.geom)
                       )
        )
        output_json = emit_bikeways_featurecollection(session, bikeways)

    print >> sys.stderr, "Length: " + str(len(output_json))

    if outfile != 'stdout':
        with open(outfile, 'w') as F:
            F.write(output_json)
    else:
        print >> sys.stdout, output_json

    sys.exit()

if __name__ == "__main__":
    main()
