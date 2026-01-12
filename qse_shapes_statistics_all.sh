#!/bin/bash

# DB100k+
python src/shapes_statistics.py \
  --shapes data/DB100k+/qse-shapes/qse_shapes_0.8_100.ttl \
  --output data/DB100k+/qse-shapes/shapes_statistics.md

# NELL-995+
python src/shapes_statistics.py \
  --shapes data/NELL-995+/qse-shapes/qse_shapes_0.8_100.ttl \
  --output data/NELL-995+/qse-shapes/shapes_statistics.md

# YAGO3-10+
python src/shapes_statistics.py \
  --shapes data/YAGO3-10+/qse-shapes/qse_shapes_0.8_100.ttl \
  --output data/YAGO3-10+/qse-shapes/shapes_statistics.md
