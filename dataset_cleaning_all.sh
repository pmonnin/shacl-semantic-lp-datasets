#!/bin/bash

# DB100k+
python src/dataset_cleaning.py \
  --input-dir data/DB100k+/original-dataset \
  --output-dir data/DB100k+/cleaned-dataset

# NELL-995+
python src/dataset_cleaning.py \
  --input-dir data/NELL-995+/original-dataset \
  --output-dir data/NELL-995+/cleaned-dataset \
  --iri-prefix http://nell.example.org/

# YAGO3-10+
python src/dataset_cleaning.py \
  --input-dir data/YAGO3-10+/original-dataset \
  --output-dir data/YAGO3-10+/cleaned-dataset
