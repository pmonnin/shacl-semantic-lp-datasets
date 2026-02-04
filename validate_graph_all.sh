#!/bin/bash

# DB100k+
python src/validate_graph.py \
  --graph data/DB100k+/reconstructed-datasets/full_dataset.ttl \
  --shapes data/DB100k+/cleaned-shapes/cleaned_shapes.ttl \
  --output-safe-iris data/DB100k+/validation-reports/validation_report_full_dataset_safe_iris.ttl \
  --output-original-iris data/DB100k+/validation-reports/validation_report_full_dataset_original_iris.ttl

python src/validate_graph.py \
  --graph data/DB100k+/reconstructed-datasets/train+schema_dataset.ttl \
  --shapes data/DB100k+/cleaned-shapes/cleaned_shapes.ttl \
  --output-safe-iris data/DB100k+/validation-reports/validation_report_train+schema_dataset_safe_iris.ttl \
  --output-original-iris data/DB100k+/validation-reports/validation_report_train+schema_dataset_original_iris.ttl

# NELL-995+
python src/validate_graph.py \
  --graph data/NELL-995+/reconstructed-datasets/full_dataset.ttl \
  --shapes data/NELL-995+/cleaned-shapes/cleaned_shapes.ttl \
  --output-safe-iris data/NELL-995+/validation-reports/validation_report_full_dataset_safe_iris.ttl \
  --output-original-iris data/NELL-995+/validation-reports/validation_report_full_dataset_original_iris.ttl

python src/validate_graph.py \
  --graph data/NELL-995+/reconstructed-datasets/train+schema_dataset.ttl \
  --shapes data/NELL-995+/cleaned-shapes/cleaned_shapes.ttl \
  --output-safe-iris data/NELL-995+/validation-reports/validation_report_train+schema_dataset_safe_iris.ttl \
  --output-original-iris data/NELL-995+/validation-reports/validation_report_train+schema_dataset_original_iris.ttl

# YAGO3-10+
python src/validate_graph.py \
  --graph data/YAGO3-10+/reconstructed-datasets/full_dataset.ttl \
  --shapes data/YAGO3-10+/cleaned-shapes/cleaned_shapes.ttl \
  --output-safe-iris data/YAGO3-10+/validation-reports/validation_report_full_dataset_safe_iris.ttl \
  --output-original-iris data/YAGO3-10+/validation-reports/validation_report_full_dataset_original_iris.ttl

python src/validate_graph.py \
  --graph data/YAGO3-10+/reconstructed-datasets/train+schema_dataset.ttl \
  --shapes data/YAGO3-10+/cleaned-shapes/cleaned_shapes.ttl \
  --output-safe-iris data/YAGO3-10+/validation-reports/validation_report_train+schema_dataset_safe_iris.ttl \
  --output-original-iris data/YAGO3-10+/validation-reports/validation_report_train+schema_dataset_original_iris.ttl
