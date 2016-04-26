SOURCE_SRS := "EPSG:26915"

TARGETS = ../tmp/ramsey.centerlines.postgis.sql \
		  ../tmp/hennepin.centerlines.postgis.sql \
		  ../tmp/cities.postgis.sql

### Create SQL for city boundaries based on Census2010 data.
###   * Convert the SHP file to postgres-friendly DB dump format.
### 

### Create SQL for blockgroup boundaries based on Census2010 data.
###   * Convert the SHP file to postgres-friendly DB dump format.
### 

../tmp/cities.postgis.sql: cities/Census2010CTus.shp
	rm -rf tmp/cities_reproject
	mkdir -p tmp/cities_reproject
	$(OGR2OGR) -F "ESRI Shapefile" -s_srs $(SOURCE_SRS) -t_srs $(TARGET_SRS) tmp/cities_reproject $^
	$(SHP2PGSQL) -c -d -D -i -W LATIN1 -I tmp/cities_reproject/Census2010CTus.shp > $@

../tmp/hennepin.centerlines.postgis.sql: henn_centerlines/LOCATION_HENNEPIN_GIS_STREET_CENTERLINE.shp
	$(OGR2OGR) -F "ESRI Shapefile" -s_srs $(SOURCE_SRS) -t_srs $(TARGET_SRS) tmp/centerlines_reproject $^
	$(SHP2PGSQL) -c -d -D -i -W LATIN1 -I tmp/centerlines_reproject/LOCATION_HENNEPIN_GIS_STREET_CENTERLINE.shp > $@

../tmp/ramsey.centerlines.postgis.sql: ramsey_streets/TRANS_Street.shp
	mkdir -p tmp/r_centerlines_reproject
	$(OGR2OGR) -F "ESRI Shapefile" -s_srs $(SOURCE_SRS) -t_srs $(TARGET_SRS) tmp/r_centerlines_reproject $^
	$(SHP2PGSQL) -c -d -D -i -W LATIN1 -I tmp/r_centerlines_reproject/TRANS_Street.shp > $@

init:
	mkdir -p tmp/r_centerlines_reproject
	mkdir -p tmp/centerlines_reproject

all: init $(TARGETS)

clean: $(TARGETS)
	rm $(TARGETS)
	rm -rf tmp/centerlines_reproject
	rm -rf tmp/r_centerlines_reproject
