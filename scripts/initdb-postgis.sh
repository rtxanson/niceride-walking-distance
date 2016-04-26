#!/bin/sh
# https://github.com/appropriate/docker-postgis/blob/master/initdb-postgis.sh

set -e

export PSQL="/Applications/Postgres.app/Contents/Versions/9.5/bin/psql -p5432"
# Perform all actions as $POSTGRES_USER
export PGUSER="$USER"
export POSTGRES_DB="walking"

# Create the 'template_postgis' template db
$PSQL --dbname="$POSTGRES_DB" <<- 'EOSQL'
CREATE DATABASE template_postgis;
UPDATE pg_database SET datistemplate = TRUE WHERE datname = 'template_postgis';
EOSQL

# Load PostGIS into both template_database and $POSTGRES_DB
for DB in template_postgis "$POSTGRES_DB"; do
	echo "Loading PostGIS extensions into $DB"
	psql --dbname="$DB" <<-'EOSQL'
		CREATE EXTENSION postgis;
		CREATE EXTENSION postgis_topology;
		CREATE EXTENSION fuzzystrmatch;
		CREATE EXTENSION postgis_tiger_geocoder;
EOSQL
done
