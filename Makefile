.PHONY: help geojson_es

MAP:=
POSTGIS_PASSWORD ?= pass
DATA_DIRECTORY ?= /home/adria/dev/pyenvs/munis/src/data


default: help
help: # http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
		@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


geojson_fr: ## Export PostGIS table to GeoJSON (fr)
	ogr2ogr -select nom,dep,insee -preserve_fid -f "GeoJSON" $(DATA_DIRECTORY)/fr.geojson PG:"host=localhost port=5433 user=munis_user dbname=munis password=$(POSTGIS_PASSWORD)" "fr"

geojson_es: ## Export PostGIS table to GeoJSON (es)
	ogr2ogr -select nameunit,nameprov,codine -preserve_fid -f "GeoJSON" $(DATA_DIRECTORY)/es.geojson PG:"host=localhost port=5433 user=munis_user dbname=munis password=$(POSTGIS_PASSWORD)" "es"

geojson_cat: ## Export PostGIS table to GeoJSON (cat)
	ogr2ogr -select nameunit,nameprov,codine -preserve_fid -where "codcomuni = '09'" -f "GeoJSON" $(DATA_DIRECTORY)/cat.geojson PG:"host=localhost port=5433 user=munis_user dbname=munis password=$(POSTGIS_PASSWORD)" "es"


tiles_fr: ## Build tiles (fr)
	docker run  -it --rm -v $(DATA_DIRECTORY):/data tippecanoe:latest tippecanoe -e /data/tiles/fr -f -l fr -z 11 -Z 3 /data/fr.geojson

tiles_es: ## Build tiles (es)
	docker run  -it --rm -v $(DATA_DIRECTORY):/data tippecanoe:latest tippecanoe -e /data/tiles/es -f -l es -z 11 -Z 3 /data/es.geojson

tiles_cat: ## Build tiles (cat)
	docker run  -it --rm -v $(DATA_DIRECTORY):/data tippecanoe:latest tippecanoe -e /data/tiles/cat -f -l cat -z 11 -Z 5 /data/cat.geojson

tiles_us: ## Build tiles (us)
	docker run  -it --rm -v $(DATA_DIRECTORY):/data tippecanoe:latest tippecanoe -e /data/tiles/us -f -l us -z 8 -Z 1 /data/us.geojson


s3_fr: ## Upload tiles to s3 (fr)
	aws --profile amercader s3 cp $(DATA_DIRECTORY)/tiles/fr s3://tiles.amercader.net/maps/vector/fr/ --recursive --content-type application/x-protobuf --content-encoding 'gzip'

s3_es: ## Upload tiles to s3 (es)
	aws --profile amercader s3 cp $(DATA_DIRECTORY)/tiles/es s3://tiles.amercader.net/maps/vector/es/ --recursive --content-type application/x-protobuf --content-encoding 'gzip'

s3_cat: ## Upload tiles to s3 (cat)
	aws --profile amercader s3 cp $(DATA_DIRECTORY)/tiles/cat s3://tiles.amercader.net/maps/vector/cat/ --recursive --content-type application/x-protobuf --content-encoding 'gzip'

s3_us: ## Upload tiles to s3 (us)
	aws --profile amercader s3 cp $(DATA_DIRECTORY)/tiles/us s3://tiles.amercader.net/maps/vector/us/ --recursive --content-type application/x-protobuf --content-encoding 'gzip'
