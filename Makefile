PSQL      := /Applications/Postgres.app/Contents/Versions/9.5/bin/psql -p5432
TOPOJSON  := ./node_modules/.bin/topojson
OGR2OGR   := /Applications/Postgres.app/Contents/Versions/9.5/bin/ogr2ogr
SHP2PGSQL := /Applications/Postgres.app/Contents/Versions/9.5/bin/shp2pgsql

##
### Makefile doc
##

# This makefile is a mess so far, but ...

### Do the actual data install, and post-install operations.
# TODO: bikeways
.PHONY: install_tables
install_tables:
	/Applications/Postgres.app/Contents/Versions/9.5/bin/psql -p5432 -d walking -f data/cities.postgis.sql
	/Applications/Postgres.app/Contents/Versions/9.5/bin/psql -p5432 -d walking -f data/stations.postgis.sql
	/Applications/Postgres.app/Contents/Versions/9.5/bin/psql -p5432 -d walking -f data/blockgroups.postgis.sql
	/Applications/Postgres.app/Contents/Versions/9.5/bin/psql -p5432 -d walking -f data/hennepin.centerlines.postgis.sql
	/Applications/Postgres.app/Contents/Versions/9.5/bin/psql -p5432 -d walking -f data/ramsey.centerlines.postgis.sql
	/Applications/Postgres.app/Contents/Versions/9.5/bin/psql -p5432 -d walking -f data/bikeways.postgis.sql
	@echo " ... This will take a while. ... "
	. env/bin/activate && python post_db_install.py
	@echo " ... DONE ... "

# vrt doc http://www.gdal.org/drv_vrt.html
# http://gis.stackexchange.com/questions/327/how-can-i-convert-an-excel-file-with-x-y-columns-to-a-shapefile
#

### ?? is this correct?
NICERIDE_SOURCE_SRS = "EPSG:4269"

### nad83 / utm zone 15n
### http://spatialreference.org/ref/epsg/nad83-utm-zone-15n/ 
NAD_1983_UTM_Zone_15N = "EPSG:26915"
CENSUS_SOURCE_SRS = "EPSG:26915"

### WGS84
TARGET_SRS = "EPSG:4326"

### Create SQL data for niceride station locations:
###   * Transform the CSV to a SHP file using the VRT definition.
###   * Convert the SHP file to postgres-friendly DB dump format.
###
data/stations.postgis.sql: data_src/bikeStations.xml
	rm -rf tmp/niceride_reproject
	rm -rf data_src/niceride_stations/
	mkdir -p data_src/niceride_stations/
	mkdir -p tmp/niceride_reproject
	cd data_src && $(OGR2OGR) -f "ESRI Shapefile" niceride_stations niceride_station_xml_to_shp.vrt
	$(OGR2OGR) -F "ESRI Shapefile" -s_srs $(NICERIDE_SOURCE_SRS) -t_srs $(TARGET_SRS) tmp/niceride_reproject data_src/niceride_stations/bikeStations.shp
	$(SHP2PGSQL) -c -d -D -i -W LATIN1 -I tmp/niceride_reproject/bikeStations.shp > $@

### Create SQL for city boundaries based on Census2010 data.
###   * Convert the SHP file to postgres-friendly DB dump format.
### 
data/cities.postgis.sql: data_src/cities/Census2010CTus.shp
	rm -rf tmp/cities_reproject
	mkdir -p tmp/cities_reproject
	$(OGR2OGR) -F "ESRI Shapefile" -s_srs $(CENSUS_SOURCE_SRS) -t_srs $(TARGET_SRS) tmp/cities_reproject $^
	$(SHP2PGSQL) -c -d -D -i -W LATIN1 -I tmp/cities_reproject/Census2010CTus.shp > $@

### Create SQL for blockgroup boundaries based on Census2010 data.
###   * Convert the SHP file to postgres-friendly DB dump format.
### 
data/blockgroups.postgis.sql: data_src/census2010/Census2010TigerBlockGroup.shp
	rm -rf tmp/blockgroups_reproject
	mkdir -p tmp/blockgroups_reproject
	$(OGR2OGR) -F "ESRI Shapefile" -s_srs $(CENSUS_SOURCE_SRS) -t_srs $(TARGET_SRS)  tmp/blockgroups_reproject $^
	$(SHP2PGSQL) -c -d -D -i -W LATIN1 -I tmp/blockgroups_reproject/Census2010TigerBlockGroup.shp > $@

data/hennepin.centerlines.postgis.sql: data_src/henn_centerlines/LOCATION_HENNEPIN_GIS_STREET_CENTERLINE.shp
	rm -rf tmp/centerlines_reproject
	mkdir -p tmp/centerlines_reproject
	$(OGR2OGR) -F "ESRI Shapefile" -s_srs $(CENSUS_SOURCE_SRS) -t_srs $(TARGET_SRS) tmp/centerlines_reproject $^
	$(SHP2PGSQL) -c -d -D -i -W LATIN1 -I tmp/centerlines_reproject/LOCATION_HENNEPIN_GIS_STREET_CENTERLINE.shp > $@

data/bikeways.postgis.sql: data_src/Bikeways/Bikeways.shp
	rm -rf tmp/bikeways_reproject
	mkdir -p tmp/bikeways_reproject
	$(OGR2OGR) -F "ESRI Shapefile" -s_srs $(CENSUS_SOURCE_SRS) -t_srs $(TARGET_SRS) tmp/bikeways_reproject $^
	$(SHP2PGSQL) -c -d -D -i -W LATIN1 -I tmp/bikeways_reproject/Bikeways.shp > $@

data/ramsey.centerlines.postgis.sql: data_src/ramsey_streets/TRANS_Street.shp
	rm -rf tmp/r_centerlines_reproject
	mkdir -p tmp/r_centerlines_reproject
	$(OGR2OGR) -F "ESRI Shapefile" -s_srs $(CENSUS_SOURCE_SRS) -t_srs $(TARGET_SRS) tmp/r_centerlines_reproject $^
	$(SHP2PGSQL) -c -d -D -i -W LATIN1 -I tmp/r_centerlines_reproject/TRANS_Street.shp > $@


### Convert blockgroup XLSX file to CSV. This will be used in the post
### install operations.
### 
data/blockgroup_population.csv: data_src/census2010/Census2010PopulationBlockGroup.xlsx
	. env/bin/activate && ./env/bin/xlsx2csv $^ $@

	  # data/bikeways.postgis.sql \
.PHONY: data
data: data/blockgroups.postgis.sql \
	  data/stations.postgis.sql \
	  data/hennepin.centerlines.postgis.sql \
	  data/ramsey.centerlines.postgis.sql \
	  data/cities.postgis.sql \
	  data/blockgroup_population.csv

### Data export process
### 
data/blockgroups.geo.json:
	. env/bin/activate && python export_to_geojson.py blockgroup $@

### Data export process
### 
data/stations.geo.json:
	. env/bin/activate && python export_to_geojson.py station $@

### Data export process
### 
data/cities.geo.json:
	. env/bin/activate && python export_to_geojson.py city $@

data/streets.geo.json:
	. env/bin/activate && python export_to_geojson.py streets $@

# data/bikeways.geo.json:
# 	. env/bin/activate && python export_to_geojson.py bikeways $@

### TopoJSON conversion process: 
###   * -p include all properties
###   * --bbox - include bounding box
###   * --id-property - set the id
###   * rest: define keys to combine data into.
### 

# NB removed: streets=data/streets.geo.json
# bikeways=data/bikeways.geo.json \
# data/bikeways.geo.json
data/blockgroups.and.cities.topo.json: data/blockgroups.geo.json \
									   data/stations.geo.json \
									   data/cities.geo.json
	$(TOPOJSON) $^ \
		--id-property id \
		--bbox -p \
		-- \
            bikeways=data/streets.geo.json \
			blockgroups=data/blockgroups.geo.json \
			cities=data/cities.geo.json \
			stations=data/stations.geo.json \
		> $@

### Copy
### 
json/blockgroups.and.cities.topo.json: data/blockgroups.and.cities.topo.json
	cp $^ $@

### Run the choropleth make process.
### 
.PHONY: choropleth
choropleth:
	cd web/ && make all

### Build all the data for web
### 
.PHONY: web
web: export \
	 json/blockgroups.and.cities.topo.json \
	 choropleth

.PHONY: geojsons
geojsons: data/blockgroups.geo.json \
		  data/stations.geo.json \
		  data/streets.geo.json \
		  data/cities.geo.json

.PHONY: topojsons
topojsons:  data/blockgroups.and.cities.topo.json

export: geojsons \
		topojsons

clean:
	rm data/*.sql
	rm -rf tmp

### Virtualenv, create dirs, install node module.
###
init:
	virtualenv env 
	. env/bin/activate && pip install -r requirements.txt
	npm install topojson
	mkdir -p data
	mkdir -p tmp

test:
	. env/bin/activate && python test_data.py

