#!/bin/bash

# DB100k+
python src/validation_reports_statistics.py \
  --report-full data/DB100k+/validation-reports/validation_report_full_dataset_original_iris.ttl \
  --report-train data/DB100k+/validation-reports/validation_report_train+schema_dataset_original_iris.ttl \
  --output data/DB100k+/validation-reports/reports_statistics.md

# NELL-995+
python src/validation_reports_statistics.py \
  --report-full data/NELL-995+/validation-reports/validation_report_full_dataset_original_iris.ttl \
  --report-train data/NELL-995+/validation-reports/validation_report_train+schema_dataset_original_iris.ttl \
  --output data/NELL-995+/validation-reports/reports_statistics.md

  # YAGO3-10+
python src/validation_reports_statistics.py \
  --report-full data/YAGO3-10+/validation-reports/validation_report_full_dataset_safe_iris.ttl \
  --report-train data/YAGO3-10+/validation-reports/validation_report_train+schema_dataset_safe_iris.ttl \
  --output data/YAGO3-10+/validation-reports/reports_statistics.md
