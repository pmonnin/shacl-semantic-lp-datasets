# shacl-semantic-lp-datasets

## Description 

Link prediction datasets based on the YAGO3-10, NELL-995, and DB100k standard link prediction datasets.

These datasets were bootstrapped from the semantically enriched version of these datasets, available on [Zenodo](https://zenodo.org/records/17438317)
and [Github](https://github.com/Wimmics/semantically-enriched-link-prediction-datasets). 
See the associated publication for more details on the semantically enriched datasets [[1]](#ref-1).

From these datasets, SHACL shapes were mined using QSE [[2]](#ref-2) and later used to enrich the link prediction datasets. 

## Dataset structure

Datasets are available in the ``data/`` folder and are structured as follows:

* The full triples contained in the dataset in **full_dataset.ttl** (groups all triples from the train/val/test splits and the TBox axioms)
* The dataset splits **train2id.txt**, **test2id.txt** and **valid2id.txt**
* The dataset splits variants including the explicit modeling of inverse relations **train2id_inv.txt**, **test2id_inv.txt** and **valid2id_inv.txt**
* a `pickle/` folder containing different __pickle__ dictionnaries
    * **ent2id** translating each entity to its related **id** (int)
    * **rel2id** translating each relation to its related **id** (int)
    * **class2id** translating each class to its related **id** (int)
    * **inst_type** linking ids of entities to their types (no inferred types included)
    * **inst_type_all** linking ids of entities to their types (including those that were got from subsumption axiom closure in any dataset, and domain/range in YAGO3-10+ and NELL-995+)
    * **classid2entid** linking ids of classes to the ids of their instances (including those that were infered from subsumption axiom closure in any dataset, and domain/range in YAGO3-10+ and NELL-995+)
    * **subclassof2id** linking ids of classes to their direct superclasses ids (set of ids)
    * **subclassof_all2id** linking ids of classes to their direct and indirect superclasses ids (set of ids)
    * **rid2domid** linking predicates ids to their related domain classes ids (set of ids)
    * **rid2rangeid** linking predicates ids to their related range classes ids (set of ids)
    * **observed_tails_original_kg** contains a head/relation/tail index of the dataset in the form of nested dictionaries using ids of entities and relations
    * **observed_heads_original_kg** contains a tail/relation/head index of the dataset in the form of nested dictionaries using ids of entities and relations
    * **observed_tails_inv** is an equivalent of **observed_tails_original_kg** that also contains explicit modelling of inverse relations
    * **observed_heads_inv** is an equivalent of **observed_heads_original_kg** that also contains explicit modelling of inverse relations

## Re-building the datasets

1. Download the [original datasets](https://zenodo.org/record/17438317)
2. Run the ``dataset_reconstruct.py`` Python script that groups all triples from the train/val/test splits and the TBox axioms (see [``reconstruct_dataset.sh``](dataset_reconstruct_all.sh)).
3. Use [QSE](https://github.com/dkw-aau/qse) to mine SHACL shapes from the datasets, using a confidence of 0.8 and a support of 100.
4. Run the ``shapes_statistics.py`` Python script to get statistics about the mined SHACL shapes (see [``stats4shapes.sh``](qse_shapes_statistics_all.sh)).

## References

1. <span id=ref-1>Nicolas Robert, Pierre Monnin, Catherine Faron. Semantically Enriched Datasets for Link Prediction:
DB100k+, NELL-995+ and YAGO3-10+. 1st International Workshop on Advanced Neuro-Symbolic
Applications Co-located with ECAI 2025, Oct 2025, Bologna, Italy. [[paper]](https://hal.science/hal-05291884v1)</span>
2. <span id=ref-2>Kashif Rabbani, Matteo Lissandrini, Katja Hose. Extraction of Validating Shapes from very large 
Knowledge Graphs. Proc. VLDB Endow. 16(5): 1023-1032 (2023). [[paper]](https://www.vldb.org/pvldb/vol16/p1023-rabbani.pdf)</span>

## Funding acknowledgement

These datasets are part of the [SHACKLE project](https://pmonnin.github.io/shackle.html) that has received funding from the European Union, via the oc2-2024-TES-02 issued and implemented by the ENFIELD project, under the grant agreement No 101120657. 