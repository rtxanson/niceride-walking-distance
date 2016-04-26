### Data export process
### 
# data/blockgroups.geo.json:
# 	. env/bin/activate && python export_to_geojson.py blockgroup $@

TARGETS := blockgroups.and.cities.topo.json

tmp/stations.geo.json:
	$(WITH_VIRTUALENV) && python $(SCRIPTS)/export_to_geojson.py station $@

tmp/cities.geo.json:
	$(WITH_VIRTUALENV) && python $(SCRIPTS)/export_to_geojson.py city $@

tmp/streets.geo.json:
	$(WITH_VIRTUALENV) && python $(SCRIPTS)/export_to_geojson.py streets $@

blockgroups.and.cities.topo.json: tmp/stations.geo.json \
								  tmp/streets.geo.json \
								  tmp/cities.geo.json
	$(shell which topojson) $^ \
		--id-property id \
		--bbox -p \
		-- \
            bikeways=tmp/streets.geo.json \
			cities=tmp/cities.geo.json \
			stations=tmp/stations.geo.json \
		> $@

export: tmp/streets.geo.json \
		tmp/cities.geo.json \
		tmp/stations.geo.json \
	    blockgroups.and.cities.topo.json

prereqs: init
	$(MAKE) -C xml
	$(MAKE) -C csv
	$(MAKE) -C shp
	$(MAKE) -C db

all: prereqs \
 	 export

init:
	mkdir -p json

clean:
	$(MAKE) -C shp clean
	rm -rf json
	rm $(TARGETS)
