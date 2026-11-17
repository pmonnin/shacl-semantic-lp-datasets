#!/bin/bash

# DB100k+
python src/validate_graph.py \
  --graph data/DB100k+/reconstructed-datasets/full_dataset.ttl \
  --shapes data/DB100k+/cleaned-shapes/cleaned_shapes.ttl \
  --output data/DB100k+/validation-reports/validation_report_full_dataset.ttl \
  --output-iri-map data/DB100k+/validation-reports/iri_map.pkl

python src/validate_graph.py \
  --graph data/DB100k+/reconstructed-datasets/train+schema_dataset.ttl \
  --shapes data/DB100k+/cleaned-shapes/cleaned_shapes.ttl \
  --output data/DB100k+/validation-reports/validation_report_train+schema_dataset.ttl

python src/validate_graph.py \
  --graph data/DB100k+/reconstructed-datasets/train+val+schema_dataset.ttl \
  --shapes data/DB100k+/cleaned-shapes/cleaned_shapes.ttl \
  --output data/DB100k+/validation-reports/validation_report_train+val+schema_dataset.ttl

# NELL-995+
python src/validate_graph.py \
  --graph data/NELL-995+/reconstructed-datasets/full_dataset.ttl \
  --shapes data/NELL-995+/cleaned-shapes/cleaned_shapes.ttl \
  --output data/NELL-995+/validation-reports/validation_report_full_dataset.ttl \
  --output-iri-map data/NELL-995+/validation-reports/iri_map.pkl

python src/validate_graph.py \
  --graph data/NELL-995+/reconstructed-datasets/train+schema_dataset.ttl \
  --shapes data/NELL-995+/cleaned-shapes/cleaned_shapes.ttl \
  --output data/NELL-995+/validation-reports/validation_report_train+schema_dataset.ttl

python src/validate_graph.py \
  --graph data/NELL-995+/reconstructed-datasets/train+val+schema_dataset.ttl \
  --shapes data/NELL-995+/cleaned-shapes/cleaned_shapes.ttl \
  --output data/NELL-995+/validation-reports/validation_report_train+val+schema_dataset.ttl

# YAGO3-10+
python src/validate_graph.py \
  --graph data/YAGO3-10+/reconstructed-datasets/full_dataset.ttl \
  --shapes data/YAGO3-10+/cleaned-shapes/cleaned_shapes.ttl \
  --output data/YAGO3-10+/validation-reports/validation_report_full_dataset.ttl \
  --output-iri-map data/YAGO3-10+/validation-reports/iri_map.pkl

python src/validate_graph.py \
  --graph data/YAGO3-10+/reconstructed-datasets/train+schema_dataset.ttl \
  --shapes data/YAGO3-10+/cleaned-shapes/cleaned_shapes.ttl \
  --output data/YAGO3-10+/validation-reports/validation_report_train+schema_dataset.ttl

python src/validate_graph.py \
  --graph data/YAGO3-10+/reconstructed-datasets/train+val+schema_dataset.ttl \
  --shapes data/YAGO3-10+/cleaned-shapes/cleaned_shapes.ttl \
  --output data/YAGO3-10+/validation-reports/validation_report_train+val+schema_dataset.ttl
