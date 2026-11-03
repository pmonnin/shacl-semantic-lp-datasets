#!/bin/bash

# Same as qse_mine_all.sh, but QSE reads its config and query files and writes its output on a fast local filesystem.
# QSE reopens the config file for each property shape and writes its shapes to an RDF4J store (db_default) in its
# output folder, which takes hours on a network filesystem (e.g., YAGO3-10+).

QSE_JAR=vendor/qse-wimmics.jar

# Use the Java runtime of the conda env (it sets JAVA_HOME) when there is one
JAVA=java
if [ -n "$JAVA_HOME" ]; then
  JAVA="$JAVA_HOME/bin/java"
fi

# Work in RAM (/dev/shm on Linux) or in the local temp dir otherwise
if [ -d /dev/shm ] && [ -w /dev/shm ]; then
  WORK_DIR=$(mktemp -d /dev/shm/qse-work.XXXXXX)
else
  WORK_DIR=$(mktemp -d "${TMPDIR:-/tmp}/qse-work.XXXXXX")
fi
trap 'rm -rf "$WORK_DIR"' EXIT
echo "QSE working dir: $WORK_DIR"

# QSE reads its SPARQL query files from resources_path on disk, so extract them from the jar
unzip -o -q $QSE_JAR 'queries/*' 'shacl_queries/*' 'shacl_stats_queries/*' 'stats/*' -d "$WORK_DIR/qse-resources"

# Run QSE with a copy of the dataset config whose output_file_path and resources_path point to the working dir, then
# copy its output back to qse-output/ (except the db_* RDF4J stores, which are only intermediate)
run_qse() {
  local dataset_dir=$1
  local dataset_name=$2
  local output_dir="$WORK_DIR/$dataset_name-output"
  local config="$WORK_DIR/${dataset_name}_qse_config.properties"

  mkdir -p "$output_dir" "$dataset_dir/qse-shapes/qse-output"
  sed -e "s|^output_file_path=.*|output_file_path=$output_dir/|" \
      -e "s|^resources_path=.*|resources_path=$WORK_DIR/qse-resources|" \
      "$dataset_dir/qse-shapes/qse_config.properties" > "$config"

  $JAVA -Xmx510g -jar $QSE_JAR "$config"

  find "$output_dir" -mindepth 1 -maxdepth 1 ! -name 'db_*' -exec cp -r {} "$dataset_dir/qse-shapes/qse-output/" \;
  rm -rf "$output_dir"
}

# QSE exits with 0 even when it fails, so only replace the shapes when it produced node shapes
copy_shapes() {
  if grep -q "NodeShape" "$1"; then
    cp "$1" "$2"
  else
    echo "ERROR: no shapes in $1, $2 left unchanged" >&2
  fi
}

# DB100k+
run_qse data/DB100k+ DB100k
copy_shapes data/DB100k+/qse-shapes/qse-output/DB100k_QSE_0.8_100_SHACL.ttl \
  data/DB100k+/qse-shapes/qse_shapes_0.8_100.ttl

# NELL-995+
run_qse data/NELL-995+ NELL-995
copy_shapes data/NELL-995+/qse-shapes/qse-output/NELL-995_QSE_0.8_100_SHACL.ttl \
  data/NELL-995+/qse-shapes/qse_shapes_0.8_100.ttl

# YAGO3-10+
run_qse data/YAGO3-10+ YAGO3-10
copy_shapes data/YAGO3-10+/qse-shapes/qse-output/YAGO3-10_QSE_0.8_100_SHACL.ttl \
  data/YAGO3-10+/qse-shapes/qse_shapes_0.8_100.ttl
