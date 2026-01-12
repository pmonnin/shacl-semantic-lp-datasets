#!/bin/bash

# DB100k+
python src/validation_reports_statistics.py \
  --shapes data/DB100k+/cleaned-shapes/cleaned_shapes.ttl \
  --report-full data/DB100k+/validation-reports/validation_report_full_dataset.ttl \
  --report-train data/DB100k+/validation-reports/validation_report_train+schema_dataset.ttl \
  --output data/DB100k+/validation-reports/reports_statistics.md

# NELL-995+
python src/validation_reports_statistics.py \
  --shapes data/NELL-995+/cleaned-shapes/cleaned_shapes.ttl \
  --report-full data/NELL-995+/validation-reports/validation_report_full_dataset.ttl \
  --report-train data/NELL-995+/validation-reports/validation_report_train+schema_dataset.ttl \
  --output data/NELL-995+/validation-reports/reports_statistics.md