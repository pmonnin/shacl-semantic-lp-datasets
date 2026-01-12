#!/bin/bash

# DB100k+
python src/shapes_cleaning.py \
  --shapes data/DB100k+/qse-shapes/qse_shapes_0.8_100.ttl \
  --output data/DB100k+/cleaned-shapes/cleaned_shapes.ttl

# NELL-995+
python src/shapes_cleaning.py \
  --shapes data/NELL-995+/qse-shapes/qse_shapes_0.8_100.ttl \
  --output data/NELL-995+/cleaned-shapes/cleaned_shapes.ttl

# YAGO3-10+
python src/shapes_cleaning.py \
  --shapes data/YAGO3-10+/qse-shapes/qse_shapes_0.8_100.ttl \
  --output data/YAGO3-10+/cleaned-shapes/cleaned_shapes.ttl
