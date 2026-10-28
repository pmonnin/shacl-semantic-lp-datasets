#!/bin/bash

QSE_JAR=vendor/qse-wimmics.jar

# QSE reads its SPARQL query files from resources_path on disk, so extract them from the jar
unzip -o -q $QSE_JAR 'queries/*' 'shacl_queries/*' 'shacl_stats_queries/*' 'stats/*' -d vendor/qse-resources

# QSE exits with 0 even when it fails, so only replace the shapes when it produced node shapes
copy_shapes() {
  if grep -q "NodeShape" "$1"; then
    cp "$1" "$2"
  else
    echo "ERROR: no shapes in $1, $2 left unchanged" >&2
  fi
}

# DB100k+
mkdir -p data/DB100k+/qse-shapes/qse-output
java -jar $QSE_JAR data/DB100k+/qse-shapes/qse_config.properties
copy_shapes data/DB100k+/qse-shapes/qse-output/DB100k_QSE_0.8_100_SHACL.ttl \
  data/DB100k+/qse-shapes/qse_shapes_0.8_100.ttl

# NELL-995+
mkdir -p data/NELL-995+/qse-shapes/qse-output
java -jar $QSE_JAR data/NELL-995+/qse-shapes/qse_config.properties
copy_shapes data/NELL-995+/qse-shapes/qse-output/NELL-995_QSE_0.8_100_SHACL.ttl \
  data/NELL-995+/qse-shapes/qse_shapes_0.8_100.ttl

# YAGO3-10+
mkdir -p data/YAGO3-10+/qse-shapes/qse-output
java -Xmx128g -jar $QSE_JAR data/YAGO3-10+/qse-shapes/qse_config.properties
copy_shapes data/YAGO3-10+/qse-shapes/qse-output/YAGO3-10_QSE_0.8_100_SHACL.ttl \
  data/YAGO3-10+/qse-shapes/qse_shapes_0.8_100.ttl
