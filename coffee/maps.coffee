require "d3"
window.queue = require "../bower_components/queue-async/queue.js"
topojson = require "topojson"


# http://stackoverflow.com/questions/31573480/scale-a-circles-radius-given-in-meters-to-d3-js-d3-geo-mercator-map

module.exports = class Mapz

  width: 1200
  height: 500
  active: d3.select(null)
  shading_attr: "DENSITY"
  radius_attr: "uses"
  radius_scale: 1

  domains:
    DENSITY: [1, 25000]
    DEFAULT: [0, 1]
    MULTRACENH: [0.007009345794392523, 0.30]

  domain_legend_labels:
    DENSITY: ["1", "25000"]
    DEFAULT: ["0%", "100%"]
    MULTRACENH: ["0%", "100%"]

  shadings:
     DENSITY:  ["white", "blue"]
     DEFAULT:  ["white", "blue"]

  make_bounds: (topo) ->
    width = @width
    height = @height
    b = @path.bounds(topo)
    s = .95 / Math.max((b[1][0] - b[0][0]) / width, (b[1][1] - b[0][1]) / height)
    t = [(width - s * (b[1][0] + b[0][0])) / 2, (height - s * (b[1][1] + b[0][1])) / 2]
    return [s, t]

  stopped: () ->
    if d3.event.defaultPrevented
      d3.event.stopPropagation()

  reset: () =>
    @active.classed("active", false)
    @active = d3.select(null)

    @svg.transition()
        .duration(750)
        .call(@zoom.translate(@initial_transl).scale(@initial_scale).event)

  zoomed: () =>
    @proj.translate(d3.event.translate).scale(d3.event.scale)
    @refresh()

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

  get_shading: (val) ->
    if @shadings[val]
      return @shadings[val]
    else
      return @shadings["DEFAULT"]

  get_domain: (val) ->
    if @domains[val]
      return @domains[val]
    else
      return @domains["DEFAULT"]

  get_domain_labels: (val) ->
    if @domain_legend_labels[val]
      return @domain_legend_labels[val]
    else
      return @domain_legend_labels["DEFAULT"]

  redrawRadiuses: () ->
    _point_scalar = (i) => i * @radius_scale

    source_quantizer = d3.scale.quantize()
                         .domain([0, 17000])
                         .range(d3.range(15).map(_point_scalar))

    set_radius = (d) =>
      if @radius_attr == "NONE"
        return 3
      q = source_quantizer(d.properties[@radius_attr])
      if q
        return q
      else
        return 2

    set_value = (d) =>
      d.properties[@radius_attr]

    # map.svg.transition()
    #     .duration(750)
    #     .style("stroke-width", 1.5 / scale + "px")
    #     .attr("transform", "translate(" + translate + ")scale(" + scale + ")")

    @station_layer.selectAll(".station")
        .transition()
        .duration(500)
        .attr("r", set_radius)

  redrawShading: () ->
    shading_domain = @get_domain(@shading_attr)
    color_range = @get_shading(@shading_attr)

    color = d3.scale.linear()
      .domain(shading_domain)
      .range(color_range)

    density = (pop, area) ->
      return (pop / area) * 2.58999e6

    window.shading_vals = []

    if @shading_attr == "DENSITY"
      density_key_setter = (d) =>
        return color(density(d.properties.POPTOTAL, d.properties.AREA))
    else if @shading_attr == "NONWHITE"
      density_key_setter = (d) =>
        pop = d.properties["POPTOTAL"]
        wnh = d.properties["WHITENH"]
        if wnh == 0
          return color(0)
        nw = d.properties["POPTOTAL"] - d.properties["WHITENH"]
        c = nw/d.properties["POPTOTAL"]
        window.shading_vals.push c
        r = color(c)
        return r
    else
      density_key_setter = (d) =>
        c = d.properties[@shading_attr]/d.properties["POPTOTAL"]
        upp = d.properties[@shading_attr]
        dun = d.properties["WHITENH"]
        if dun == 0
          return color(0)
        window.shading_vals.push c
        r = color(c)
        return r

    @bg_layer
        .selectAll("path")
        .transition()
        .duration(550)
        .style("fill", density_key_setter)

    [leg_min, leg_max] = @get_domain_labels(@shading_attr)

    @svg.selectAll('.shader-label-0').text(leg_min)
    @svg.selectAll('.shader-label-5').text(leg_max)

    @refresh()

    return

  update_legend: (d) ->
    if not @legend_box
      @legend_layer = @svg.append("g")
      @legend_box = @svg.append("g")

      @legend_box = @legend_layer
        .attr("class", "info_box")
        .attr("width", 70)
        .attr("height", 170)
        .attr("transform", "translate(5,5)")

      @legend_box.append("text")
        .text("omg")

  display_station_info: (d) ->
    $('.info-box').hide()
    info = $('#niceridestation_info_block')
    info.find('.value').html("&nbsp;")

    # Set values of fields that are not calculated
    set_info_val = (k, v) =>
      exists = info.find("[data-display=#{k}] span.value")
      if exists
          exists.html(v)
      return true

    set_info_val(k, v) for k, v of d.properties

    info.show()

  display_street_info: (d) ->
    $('.info-box').hide()
    info = $('#street_info_block')
    info.find('.value').html("&nbsp;")

    # Set values of fields that are not calculated
    set_info_val = (k, v) =>
      exists = info.find("[data-display=#{k}] span.value")
      if exists
          exists.html(v)
      return true

    set_info_val(k, v) for k, v of d.properties

    info.show()

  display_blockgroup_info: (d) ->
    $('.info-box').hide()
    info = $('#blockgroup_info_block')
    info.find('.value').html("&nbsp;")

    # Set values of fields that are not calculated
    set_info_val = (k, v) =>
      exists = info.find("[data-display=#{k}] span.value")
      if exists
          exists.html(v)
      return true

    set_info_val(k, v) for k, v of d.properties

    info.show()

    #
    # calculated fields
    #

    # TODO: format
    field_calculators =
      NONWHITE: (d) ->
        nw = d.properties["POPTOTAL"] - d.properties["WHITENH"]
        return nw
      DENSITY: (d) ->
        density = (pop, area) ->
          # (people) / (sq meters) * (sq meters / mi)
          d = (pop / area) * 2.58999e6
          # density / blocks per sq. mile
          return Math.floor(d / 16)
        return density(d.properties.POPTOTAL, d.properties.AREA)

    for calc_field in info.find('.calculated')
      attr = $(calc_field).attr('data-attr')
      func = field_calculators[attr]
      $(calc_field).find('.value').html(func(d)) if func

  draw: (json) ->
    console.log "drawing"
    boundary_path = "blockgroups.geo"

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
             # .attr("preserveAspectRatio", "xMinYMin meet")
             # .on("click", @stopped, true)

    # @svg.append("rect")
    #    .attr("class", "background")
    #    .attr("width", @width)
    #    .attr("height", @height)
    # .on("click", @reset)

    @zoom = d3.behavior.zoom()
        .translate(@proj.translate())
        .scale(@proj.scale())
        .scaleExtent([109151, 750000])
        # .on("zoom", @zoomed)
    
    @svg.call(@zoom)
        .call(@zoom.event)

    # block_group_layer = @svg.append("g")
    # @layers.push block_group_layer
    # @bg_layer = block_group_layer

    # comparator = (a, b) ->  return a != b

    # density_min = 0
    # density_max = .01
    # quanta = d3.scale.quantize()
    #            .domain([density_min, density_max])
    #            .range(d3.range(9).map( (i) => "q#{i}-9" ))

    shading_domain = @get_domain(@shading_attr)
    color_range = @get_shading(@shading_attr)

    # color = d3.scale.linear()
    #   .domain(shading_domain)
    #   .range(color_range)

    # density = (pop, area) ->
    #   d = (pop / area) * 2.58999e6
    #   return d

    # if @shading_attr == 'DENSITY'
    #   density_key_setter = (d) =>
    #     return color(density(d.properties.POPTOTAL, d.properties.AREA))
    # else
    #   density_key_setter = (d) =>
    #     return color(d.properties[@shading_attr]/d.properties["POPTOTAL"])

    # window.active = d3.select(null)

    # @bg_layer
    #     .selectAll("path")
    #     .data(topo.features)
    #     .enter().append("path")
    #     .style("fill", density_key_setter)
    #     .attr("class", "blockgroup")
    #     .attr("d", @path)
    #     # .on("click", blockgroup_click)

    ## Bikeways
    #
    # bikeway_path_layer = @svg.append("g")
    # @layers.push bikeway_path_layer

    # bikeway_topo = topojson.feature(
    #   json,
    #   json.objects['bikeways.geo']
    # )

    # set_bikeway_text = (d) ->
    #     return d.properties.name

    # bikeway_click = (d) ->
    #   # `d` is the data object, `@` is the path clicked.
    #   active = window.active
    #   map = window.m

    #   if (window.active.node() == @)
    #     return window.map.reset()
    #   $('.active').removeClass("active")
    #   window.active.classed("active", false)
    #   window.active = d3.select(@).classed("active", true)
    #   map.display_bikeway_info(d)

    # bikeway_path_layer
    #     .selectAll("path")
    #     .data(bikeway_topo.features)
    #     .enter().append("path")
    #     .attr("d", @path)
    #     .attr("class", "bikeway")
    #     .attr("style", "display: none;")
    #     .on("click", bikeway_click)
    #     .append("svg:title")
    #     .text(set_bikeway_text)
    
    ## /Bikeways

    # street_path_layer = @svg.append("g")
    # @layers.push street_path_layer

    # street_topo = topojson.feature(
    #   json,
    #   json.objects['streets.geo']
    # )

    # set_street_text = (d) ->
    #     return d.properties.name

    # street_click = (d) ->
    #   # `d` is the data object, `@` is the path clicked.
    #   active = window.active
    #   map = window.m

    #   if (window.active.node() == @)
    #     return window.map.reset()
    #   $('.active').removeClass("active")
    #   window.active.classed("active", false)
    #   window.active = d3.select(@).classed("active", true)
    #   map.display_street_info(d)

    # street_path_layer
    #     .selectAll("path")
    #     .data(street_topo.features)
    #     .enter().append("path")
    #     .attr("d", @path)
    #     .attr("class", "street")
    #     .on("click", street_click)
    #     .append("svg:title")
    #     .text(set_street_text)

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

    # source_quantizer = d3.scale.quantize()
    #                      .domain([0, 17000])
    #                      .range(d3.range(2, 17).map(_point_scalar))

    # window.rad_by_size = {}

    # set_radius = (d) =>
    #   q = source_quantizer(d.properties['uses'])
    #   window.rad_by_size[d.properties['uses']] = q
    #   if q
    #     return q
    #   else
    #     return 2

    # set_value = (d) ->
    #   d.properties['uses']

    # point_color = d3.scale.linear()
    #   .domain([11, 35])
    #   .range(["black", "red"])

    # dock_count_color = (d) ->
    #   return point_color(d.properties.dock_count)

    # set_station_text = (d) ->
    #   station_name = d.properties.name
    #   return "#{station_name}: #{d.properties.dock_count} bike docks, #{d.properties.uses} uses"

    # # station_click = (d) ->
    # #   # `d` is the data object, `@` is the path clicked.
    # #   active = window.active
    # #   map = window.m

    # #   if (window.active.node() == @)
    # #     return window.map.reset()
    # #   window.active.classed("active", false)
    # #   window.active = d3.select(@).classed("active", true)
    # #   map.display_station_info(d)

    p_transform = (d) =>
      lat_lng = @proj(d.geometry.coordinates)
      return "translate(#{lat_lng})"

    @station_layer.selectAll("stations")
        .data(station_topo.features)
        .enter().append("circle")
        .attr("class", "station")
        .attr("transform", p_transform)

    _transform_to_centroid_geom = (d) =>
      "translate(#{@path.centroid(d.geometry)})"

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

    radius = (d) =>
      _rad = d3.scale.quantize()
               .domain([0, 17000])
               .range(d3.range(2, 17).map(_point_scalar))
      # _rad = d3.scale.sqrt()
      #   .domain([0, 20000])
      #   .range([0, 15])
      return _rad(d) * @radius_scale
    # /CITIES

    console.log "ohai"
