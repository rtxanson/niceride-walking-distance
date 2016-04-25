d3 = require "d3"

queue = require "../bower_components/queue-async/queue.js"
topojson = require "topojson"
pixelLength = require "./pixel_utils.coffee"

# http://stackoverflow.com/questions/31573480/scale-a-circles-radius-given-in-meters-to-d3-js-d3-geo-mercator-map

module.exports = class Mapz

  width: 1200
  height: 500
  radius_scale: 1
  station_radius_miles: .25

  make_bounds: (topo) ->
    width = @width
    height = @height
    b = @path.bounds(topo)
    s = 1.20 / Math.max((b[1][0] - b[0][0]) / width, (b[1][1] - b[0][1]) / height)
    t = [(width - s * (b[1][0] + b[0][0])) / 2, (height - s * (b[1][1] + b[0][1])) / 2]
    return [s, t]

  redrawRadiuses: () =>
    # Redetermine the radius
    if !map.station_layer
      return
    pixels_per_hundred_1 = pixelLength(@main_topo, @proj, @station_radius_miles)
    map.station_layer.selectAll(".station")
        .attr("r", pixels_per_hundred_1)

  zoomed: () =>
    @proj.translate(d3.event.translate).scale(d3.event.scale)
    @refresh()
    @redrawRadiuses()

  refresh: () ->
    for g in @layers
      if g.print_path
        g.selectAll("path").attr("d", g.print_path)
      else
        g.selectAll("path").attr("d", @path)
      if g.retransform
        p_transform = (d) =>
          lat_lng = @proj(d.geometry.coordinates)
          return "translate(#{lat_lng})"
        g.selectAll("circle")
            .attr("transform", p_transform)
        g.selectAll("text")
            .attr("transform", p_transform)

  constructor: (@element) ->
    @width = $(@element).width()
    @layers = []

    @proj = d3.geo.mercator()
                  .scale(1)
                  .translate([0, 0])
    @path = d3.geo.path()
                  .projection(@proj)

    q = queue().defer( d3.json
                     , "./json/blockgroups.and.cities.topo.json"
                     )
    q.await(@handleRequest)

  handleRequest: (error, json) =>
    @json = json
    @draw(json)

  draw: (json) ->
    console.log "drawing"
    boundary_path = "cities.geo"

    topo = topojson.feature(
      json,
      json.objects[boundary_path]
    )

    @main_topo = topo

    features = topo.features

    [scale, translate] = @make_bounds(topo)

    @initial_scale = scale
    @initial_transl = translate

    @proj.scale(scale)
         .translate(translate)

    @svg = d3.select(@element)
             .append("svg")
             .attr("preserveAspectRatio", "xMinYMin meet")

    @zoom = d3.behavior.zoom()
        .translate(@proj.translate())
        .scale(@proj.scale())
        .scaleExtent([109151, 750000])
        .on("zoom", @zoomed)
    
    @svg.call(@zoom)
        .call(@zoom.event)

    ## BIKEWAYS
    #
    bikeway_path_layer = @svg.append("g")
    @layers.push bikeway_path_layer

    bikeway_topo = topojson.feature(
      json,
      json.objects['bikeways']
    )

    bikeway_path_layer
        .selectAll("path")
        .data(bikeway_topo.features)
        .enter().append("path")
        .attr("d", @path)
        .attr("class", "bikeway")
    # /BIKEWAYS

    # STATIONS
    @station_layer = @svg.append("g")
    @station_layer.retransform = true

    @layers.push @station_layer

    station_topo = topojson.feature(
      json,
      json.objects["stations.geo"]
    )

    p_transform = (d) =>
      lat_lng = @proj(d.geometry.coordinates)
      return "translate(#{lat_lng})"

    _point_scalar = (i) => i * @radius_scale

    p_transform = (d) =>
      lat_lng = @proj(d.geometry.coordinates)
      return "translate(#{lat_lng})"
    
    # quarter mile
    station_radius_pixels = pixelLength(@main_topo, @proj, @station_radius_miles)

    @station_layer.selectAll("stations")
        .data(station_topo.features)
        .enter().append("circle")
        .attr("r", station_radius_pixels)
        .attr("class", "station")
        .attr("transform", p_transform)

    _transform_to_centroid_geom = (d) =>
      "translate(#{@path.centroid(d.geometry)})"
    # /STATIONS

    # CITIES
    city_path_layer = @svg.append("g")
    @layers.push city_path_layer

    city_topo = topojson.feature(
      json,
      json.objects['cities.geo']
    )

    city_path_layer
        .selectAll("path")
        .data(city_topo.features)
        .enter().append("path")
        .attr("d", @path)
        .attr("class", "city")

    console.log "ohai"
    # /CITIES
