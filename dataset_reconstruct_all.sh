#!/bin/bash

# DB100k+
python src/dataset_reconstruct.py \
  --train-triples data/DB100k+/cleaned-dataset/train2id.txt \
  --val-triples data/DB100k+/cleaned-dataset/valid2id.txt \
  --test-triples data/DB100k+/cleaned-dataset/test2id.txt \
  --inst-triples data/DB100k+/cleaned-dataset/pickle/inst_type.pkl \
  --sub-triples data/DB100k+/cleaned-dataset/pickle/subclassof2id.pkl \
  --r2domid data/DB100k+/cleaned-dataset/pickle/rid2domid.pkl \
  --r2rangeid data/DB100k+/cleaned-dataset/pickle/rid2rangeid.pkl \
  --ent2id data/DB100k+/cleaned-dataset/pickle/ent2id.pkl \
  --rel2id data/DB100k+/cleaned-dataset/pickle/rel2id.pkl \
  --class2id data/DB100k+/cleaned-dataset/pickle/class2id.pkl \
  --output data/DB100k+/reconstructed-datasets/full_dataset.ttl

python src/dataset_reconstruct.py \
  --train-triples data/DB100k+/cleaned-dataset/train2id.txt \
  --inst-triples data/DB100k+/cleaned-dataset/pickle/inst_type.pkl \
  --sub-triples data/DB100k+/cleaned-dataset/pickle/subclassof2id.pkl \
  --r2domid data/DB100k+/cleaned-dataset/pickle/rid2domid.pkl \
  --r2rangeid data/DB100k+/cleaned-dataset/pickle/rid2rangeid.pkl \
  --ent2id data/DB100k+/cleaned-dataset/pickle/ent2id.pkl \
  --rel2id data/DB100k+/cleaned-dataset/pickle/rel2id.pkl \
  --class2id data/DB100k+/cleaned-dataset/pickle/class2id.pkl \
  --output data/DB100k+/reconstructed-datasets/train+schema_dataset.ttl

python src/dataset_reconstruct.py \
  --train-triples data/DB100k+/cleaned-dataset/train2id.txt \
  --val-triples data/DB100k+/cleaned-dataset/valid2id.txt \
  --inst-triples data/DB100k+/cleaned-dataset/pickle/inst_type.pkl \
  --sub-triples data/DB100k+/cleaned-dataset/pickle/subclassof2id.pkl \
  --r2domid data/DB100k+/cleaned-dataset/pickle/rid2domid.pkl \
  --r2rangeid data/DB100k+/cleaned-dataset/pickle/rid2rangeid.pkl \
  --ent2id data/DB100k+/cleaned-dataset/pickle/ent2id.pkl \
  --rel2id data/DB100k+/cleaned-dataset/pickle/rel2id.pkl \
  --class2id data/DB100k+/cleaned-dataset/pickle/class2id.pkl \
  --output data/DB100k+/reconstructed-datasets/train+val+schema_dataset.ttl

# NELL-995+
python src/dataset_reconstruct.py \
  --train-triples data/NELL-995+/cleaned-dataset/train2id.txt \
  --val-triples data/NELL-995+/cleaned-dataset/valid2id.txt \
  --test-triples data/NELL-995+/cleaned-dataset/test2id.txt \
  --inst-triples data/NELL-995+/cleaned-dataset/pickle/inst_type.pkl \
  --sub-triples data/NELL-995+/cleaned-dataset/pickle/subclassof2id.pkl \
  --r2domid data/NELL-995+/cleaned-dataset/pickle/rid2domid.pkl \
  --r2rangeid data/NELL-995+/cleaned-dataset/pickle/rid2rangeid.pkl \
  --ent2id data/NELL-995+/cleaned-dataset/pickle/ent2id.pkl \
  --rel2id data/NELL-995+/cleaned-dataset/pickle/rel2id.pkl \
  --class2id data/NELL-995+/cleaned-dataset/pickle/class2id.pkl \
  --output data/NELL-995+/reconstructed-datasets/full_dataset.ttl

python src/dataset_reconstruct.py \
  --train-triples data/NELL-995+/cleaned-dataset/train2id.txt \
  --inst-triples data/NELL-995+/cleaned-dataset/pickle/inst_type.pkl \
  --sub-triples data/NELL-995+/cleaned-dataset/pickle/subclassof2id.pkl \
  --r2domid data/NELL-995+/cleaned-dataset/pickle/rid2domid.pkl \
  --r2rangeid data/NELL-995+/cleaned-dataset/pickle/rid2rangeid.pkl \
  --ent2id data/NELL-995+/cleaned-dataset/pickle/ent2id.pkl \
  --rel2id data/NELL-995+/cleaned-dataset/pickle/rel2id.pkl \
  --class2id data/NELL-995+/cleaned-dataset/pickle/class2id.pkl \
  --output data/NELL-995+/reconstructed-datasets/train+schema_dataset.ttl

python src/dataset_reconstruct.py \
  --train-triples data/NELL-995+/cleaned-dataset/train2id.txt \
  --val-triples data/NELL-995+/cleaned-dataset/valid2id.txt \
  --inst-triples data/NELL-995+/cleaned-dataset/pickle/inst_type.pkl \
  --sub-triples data/NELL-995+/cleaned-dataset/pickle/subclassof2id.pkl \
  --r2domid data/NELL-995+/cleaned-dataset/pickle/rid2domid.pkl \
  --r2rangeid data/NELL-995+/cleaned-dataset/pickle/rid2rangeid.pkl \
  --ent2id data/NELL-995+/cleaned-dataset/pickle/ent2id.pkl \
  --rel2id data/NELL-995+/cleaned-dataset/pickle/rel2id.pkl \
  --class2id data/NELL-995+/cleaned-dataset/pickle/class2id.pkl \
  --output data/NELL-995+/reconstructed-datasets/train+val+schema_dataset.ttl

# YAGO3-10+
python src/dataset_reconstruct.py \
  --train-triples data/YAGO3-10+/cleaned-dataset/train2id.txt \
  --val-triples data/YAGO3-10+/cleaned-dataset/valid2id.txt \
  --test-triples data/YAGO3-10+/cleaned-dataset/test2id.txt \
  --inst-triples data/YAGO3-10+/cleaned-dataset/pickle/inst_type.pkl \
  --sub-triples data/YAGO3-10+/cleaned-dataset/pickle/subclassof2id.pkl \
  --r2domid data/YAGO3-10+/cleaned-dataset/pickle/rid2domid.pkl \
  --r2rangeid data/YAGO3-10+/cleaned-dataset/pickle/rid2rangeid.pkl \
  --ent2id data/YAGO3-10+/cleaned-dataset/pickle/ent2id.pkl \
  --rel2id data/YAGO3-10+/cleaned-dataset/pickle/rel2id.pkl \
  --class2id data/YAGO3-10+/cleaned-dataset/pickle/class2id.pkl \
  --output data/YAGO3-10+/reconstructed-datasets/full_dataset.ttl

python src/dataset_reconstruct.py \
  --train-triples data/YAGO3-10+/cleaned-dataset/train2id.txt \
  --inst-triples data/YAGO3-10+/cleaned-dataset/pickle/inst_type.pkl \
  --sub-triples data/YAGO3-10+/cleaned-dataset/pickle/subclassof2id.pkl \
  --r2domid data/YAGO3-10+/cleaned-dataset/pickle/rid2domid.pkl \
  --r2rangeid data/YAGO3-10+/cleaned-dataset/pickle/rid2rangeid.pkl \
  --ent2id data/YAGO3-10+/cleaned-dataset/pickle/ent2id.pkl \
  --rel2id data/YAGO3-10+/cleaned-dataset/pickle/rel2id.pkl \
  --class2id data/YAGO3-10+/cleaned-dataset/pickle/class2id.pkl \
  --output data/YAGO3-10+/reconstructed-datasets/train+schema_dataset.ttl

python src/dataset_reconstruct.py \
  --train-triples data/YAGO3-10+/cleaned-dataset/train2id.txt \
  --val-triples data/YAGO3-10+/cleaned-dataset/valid2id.txt \
  --inst-triples data/YAGO3-10+/cleaned-dataset/pickle/inst_type.pkl \
  --sub-triples data/YAGO3-10+/cleaned-dataset/pickle/subclassof2id.pkl \
  --r2domid data/YAGO3-10+/cleaned-dataset/pickle/rid2domid.pkl \
  --r2rangeid data/YAGO3-10+/cleaned-dataset/pickle/rid2rangeid.pkl \
  --ent2id data/YAGO3-10+/cleaned-dataset/pickle/ent2id.pkl \
  --rel2id data/YAGO3-10+/cleaned-dataset/pickle/rel2id.pkl \
  --class2id data/YAGO3-10+/cleaned-dataset/pickle/class2id.pkl \
  --output data/YAGO3-10+/reconstructed-datasets/train+val+schema_dataset.ttl
