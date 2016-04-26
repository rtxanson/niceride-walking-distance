PSQL := /Applications/Postgres.app/Contents/Versions/9.5/bin/psql -p5432
DB   := walking

SQLs := ../tmp/cities.postgis.sql \
		../tmp/stations.postgis.sql \
		../tmp/hennepin.centerlines.postgis.sql \
		../tmp/ramsey.centerlines.postgis.sql

FAKE_TARGETS := $(SQLs:%.sql=tmp/%.installed_sql)

TARGETS := $(FAKE_TARGETS)

.PHONY: install_tables
tmp/%.installed_sql: ../tmp/%.sql
	@echo $(PSQL) -d $(DB) -f $^
	touch $@

.PHONY: post_install
post_install:
	$(WITH_VIRTUALENV) && python $(SCRIPTS)/post_db_install.py
	@echo " ... DONE ... "

all: init \
	 $(TARGETS) \
	 post_install

init:
	mkdir tmp
	@echo " ... This will take a while. ... "

