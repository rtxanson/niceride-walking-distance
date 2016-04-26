require "d3"

# https://bl.ocks.org/thomasthoren/6a543c4d804f35a240f9

pixelLength = (this_topojson, this_projection, miles) ->
  # Calculates the window pixel length for a given map distance.
  # Not sure if math is okay, given arcs, projection distortion, etc.

  actual_map_bounds = d3.geo.bounds(this_topojson)

  radians = d3.geo.distance(actual_map_bounds[0], actual_map_bounds[1])
  earth_radius = 3959  # miles
  arc_length = earth_radius * radians  # s = r * theta

  projected_map_bounds = [
    this_projection(actual_map_bounds[0]),
    this_projection(actual_map_bounds[1])
  ]

  projected_map_width = projected_map_bounds[1][0] - projected_map_bounds[0][0]
  projected_map_height = projected_map_bounds[0][1] - projected_map_bounds[1][1]
  projected_map_hypotenuse = Math.sqrt(
    (Math.pow(projected_map_width, 2)) + (Math.pow(projected_map_height, 2))
  )

  pixels_per_mile = projected_map_hypotenuse / arc_length
  pixel_distance = pixels_per_mile * miles

  return pixel_distance

module.exports = pixelLength
