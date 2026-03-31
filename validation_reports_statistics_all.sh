#!/bin/bash

# DB100k+
python src/validation_reports_statistics.py \
  --report-full data/DB100k+/validation-reports/validation_report_full_dataset_original_iris.ttl \
  --report-train data/DB100k+/validation-reports/validation_report_train+schema_dataset_original_iris.ttl \
  --report-train-val data/DB100k+/validation-reports/validation_report_train+val+schema_dataset_original_iris.ttl \
  --output-md data/DB100k+/validation-reports/reports_statistics.md \
  --output-nc-nodes-full data/DB100k+/validation-reports/non_conformant_nodes_full.pkl \
  --output-nc-nodes-train data/DB100k+/validation-reports/non_conformant_nodes_train.pkl \
  --output-nc-nodes-train-val data/DB100k+/validation-reports/non_conformant_nodes_train+val.pkl

# NELL-995+
python src/validation_reports_statistics.py \
  --report-full data/NELL-995+/validation-reports/validation_report_full_dataset_original_iris.ttl \
  --report-train data/NELL-995+/validation-reports/validation_report_train+schema_dataset_original_iris.ttl \
  --report-train-val data/NELL-995+/validation-reports/validation_report_train+val+schema_dataset_original_iris.ttl \
  --output-md data/NELL-995+/validation-reports/reports_statistics.md \
  --output-nc-nodes-full data/NELL-995+/validation-reports/non_conformant_nodes_full.pkl \
  --output-nc-nodes-train data/NELL-995+/validation-reports/non_conformant_nodes_train.pkl \
  --output-nc-nodes-train-val data/NELL-995+/validation-reports/non_conformant_nodes_train+val.pkl

  # YAGO3-10+
python src/validation_reports_statistics.py \
  --report-full data/YAGO3-10+/validation-reports/validation_report_full_dataset_safe_iris.ttl \
  --report-train data/YAGO3-10+/validation-reports/validation_report_train+schema_dataset_safe_iris.ttl \
  --report-train-val data/YAGO3-10+/validation-reports/validation_report_train+val+schema_dataset_safe_iris.ttl \
  --output-md data/YAGO3-10+/validation-reports/reports_statistics.md \
  --output-nc-nodes-full data/YAGO3-10+/validation-reports/non_conformant_nodes_full.pkl \
  --output-nc-nodes-train data/YAGO3-10+/validation-reports/non_conformant_nodes_train.pkl \
  --output-nc-nodes-train-val data/YAGO3-10+/validation-reports/non_conformant_nodes_train+val.pkl
