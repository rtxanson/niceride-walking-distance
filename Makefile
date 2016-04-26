export OGR2OGR   := /Applications/Postgres.app/Contents/Versions/9.5/bin/ogr2ogr
export SHP2PGSQL := /Applications/Postgres.app/Contents/Versions/9.5/bin/shp2pgsql

export WITH_VIRTUALENV := . $(shell pwd)/env/bin/activate
export SCRIPTS := $(shell pwd)/scripts
export WEBPACK := $(shell which webpack)

##
### Makefile doc
##

# vrt doc http://www.gdal.org/drv_vrt.html
# http://gis.stackexchange.com/questions/327/how-can-i-convert-an-excel-file-with-x-y-columns-to-a-shapefile
#

### nad83 / utm zone 15n
### http://spatialreference.org/ref/epsg/nad83-utm-zone-15n/ 
# NAD_1983_UTM_Zone_15N = "EPSG:26915"
# CENSUS_SOURCE_SRS = "EPSG:26915"

### WGS84
export TARGET_SRS = "EPSG:4326"

.PHONY: data
data:
	make -C data all


### TopoJSON conversion process: 
###   * -p include all properties
###   * --bbox - include bounding box
###   * --id-property - set the id
###   * rest: define keys to combine data into.
### 

### Copy
### 
json/blockgroups.and.cities.topo.json: data/blockgroups.and.cities.topo.json
	cp $^ $@

### Build all the data for web
### 
.PHONY: web
web: json/blockgroups.and.cities.topo.json \
	 assets

.PHONY: assets
assets:
	$(MAKE) -C web

clean:
	$(MAKE) -C data clean
	$(MAKE) -C web clean
	rm -rf node_modules
	rm data/*.sql
	rm -rf tmp

### Virtualenv, create dirs, install node module.
###
init:
	virtualenv env 
	. env/bin/activate && pip install -r requirements.txt
	npm install
	$(MAKE) -C web init
	mkdir -p data
	mkdir -p json
	mkdir -p tmp

test:
	. env/bin/activate && python test_data.py

