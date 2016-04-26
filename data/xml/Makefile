NICERIDE_SOURCE_SRS := "EPSG:4269"

TARGETS := ../tmp/bikeStations.csv

### Create SQL data for niceride station locations:
###   * Transform the CSV to a SHP file using the VRT definition.
###   * Convert the SHP file to postgres-friendly DB dump format.
###

# ../sql/stations.postgis.sql: bikeStations.xml
# 	rm -rf tmp/niceride_reproject
# 	rm -rf data_src/niceride_stations/
# 	mkdir -p data_src/niceride_stations/
# 	mkdir -p tmp/niceride_reproject
# 	cd data_src && $(OGR2OGR) -f "ESRI Shapefile" niceride_stations niceride_station_xml_to_shp.vrt
# 	$(OGR2OGR) -F "ESRI Shapefile" -s_srs $(NICERIDE_SOURCE_SRS) -t_srs $(TARGET_SRS) tmp/niceride_reproject data_src/niceride_stations/bikeStations.shp
# 	$(SHP2PGSQL) -c -d -D -i -W LATIN1 -I tmp/niceride_reproject/bikeStations.shp > $@

../tmp/bikeStations.csv: bikeStations.xml
	xml2csv --input "$^" --output "$@" --tag "station"

all: $(TARGETS)

clean:
	rm $(TARGETS)
