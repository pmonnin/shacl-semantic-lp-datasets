#!/bin/bash

# DB100k+
pyshacl -s data/DB100k+/cleaned-shapes/cleaned_shapes.ttl \
  -i none -f turtle \
  -o data/DB100k+/validation-reports/validation_report_train+schema_dataset.ttl \
  data/DB100k+/reconstructed-datasets/train+schema_dataset.ttl

# NELL-995+
pyshacl -s data/NELL-995+/cleaned-shapes/cleaned_shapes.ttl \
  -i none -f turtle \
  -o data/NELL-995+/validation-reports/validation_report_train+schema_dataset.ttl \
  data/NELL-995+/reconstructed-datasets/train+schema_dataset.ttl

# YAGO3-10+
pyshacl -s data/YAGO3-10+/cleaned-shapes/cleaned_shapes.ttl \
  -i none -f turtle \
  -o data/YAGO3-10+/validation-reports/validation_report_train+schema_dataset.ttl \
  data/YAGO3-10+/reconstructed-datasets/train+schema_dataset.ttl
