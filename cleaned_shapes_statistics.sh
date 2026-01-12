#!/bin/bash

# DB100k+
python src/shapes_statistics.py \
  --shapes data/DB100k+/cleaned-shapes/cleaned_shapes.ttl \
  --output data/DB100k+/cleaned-shapes/shapes_statistics.md

# NELL-995+
python src/shapes_statistics.py \
  --shapes data/NELL-995+/cleaned-shapes/cleaned_shapes.ttl \
  --output data/NELL-995+/cleaned-shapes/shapes_statistics.md

# YAGO3-10+
python src/shapes_statistics.py \
  --shapes data/YAGO3-10+/cleaned-shapes/cleaned_shapes.ttl \
  --output data/YAGO3-10+/cleaned-shapes/shapes_statistics.md
