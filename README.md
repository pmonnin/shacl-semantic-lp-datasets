# shacl-semantic-lp-datasets

Link prediction datasets based on the YAGO3-10, NELL-995, and DB100k standard link prediction datasets, enriched with RDFS semantics and SHACL shapes.

## Description 

Link prediction datasets based on the YAGO3-10, NELL-995, and DB100k standard link prediction datasets.

These datasets were bootstrapped from the semantically enriched version of these datasets, available on [Zenodo](https://zenodo.org/records/17438317)
and [Github](https://github.com/Wimmics/semantically-enriched-link-prediction-datasets). 
See the associated publication for more details on the semantically enriched datasets [[1]](#ref-1).

From these datasets, SHACL shapes were mined using QSE [[2]](#ref-2) and later used to enrich the link prediction datasets. 

## Dataset structure

Datasets are available in the ``data/`` folder and are structured as follows:

* The ``original-dataset/`` folder contains the original dataset: 
    * The dataset splits **train2id.txt**, **test2id.txt** and **valid2id.txt**
    * The dataset splits variants including the explicit modeling of inverse relations **train2id_inv.txt**, **test2id_inv.txt** and **valid2id_inv.txt**
    * a `pickle/` folder containing different __pickle__ dictionaries
      * **ent2id** translating each entity to its related **id** (int)
      * **rel2id** translating each relation to its related **id** (int)
      * **class2id** translating each class to its related **id** (int)
      * **inst_type** linking ids of entities to their types (no inferred types included)
      * **inst_type_all** linking ids of entities to their types (including those that were got from subsumption axiom closure in any dataset, and domain/range in YAGO3-10+ and NELL-995+)
      * **classid2entid** linking ids of classes to the ids of their instances (including those that were inferred from subsumption axiom closure in any dataset, and domain/range in YAGO3-10+ and NELL-995+)
      * **subclassof2id** linking ids of classes to their direct superclasses ids (set of ids)
      * **subclassof_all2id** linking ids of classes to their direct and indirect superclasses ids (set of ids)
      * **rid2domid** linking predicates ids to their related domain classes ids (set of ids)
      * **rid2rangeid** linking predicates ids to their related range classes ids (set of ids)
      * **observed_tails_original_kg** contains a head/relation/tail index of the dataset in the form of nested dictionaries using ids of entities and relations
      * **observed_heads_original_kg** contains a tail/relation/head index of the dataset in the form of nested dictionaries using ids of entities and relations
      * **observed_tails_inv** is an equivalent of **observed_tails_original_kg** that also contains explicit modeling of inverse relations
      * **observed_heads_inv** is an equivalent of **observed_heads_original_kg** that also contains explicit modeling of inverse relations
* The ``cleaned-dataset/`` folder has the same structure as ``original-dataset/`` and contains the cleaned original dataset (see [Re-building the datasets](#re-building-the-datasets))
* The ``reconstructed-datasets/`` folder contains: 
  * The full dataset grouping triples from the train/val/test splits and the TBox axioms
  * The train+TBox dataset
  * The train+val+TBox dataset
* The ``qse-shapes/`` folder contains the SHACL shapes mined by QSE on the full dataset, and their statistics 
* The ``cleaned-shapes/`` folder contains the cleaned SHACL shapes and their statistics (removing shapes involving ``rdf:type`` paths)
* The ``validation-reports/`` folder contains the validation reports and their statistics for the full dataset and the train+TBox dataset using original IRIs and safe IRIs (where invalid characters are URL encoded)

## Re-building the datasets

1. Download the [original datasets](https://zenodo.org/record/17438317)
2. Clean the original datasets
   * Values of the pickles linking ids to sets of ids (**inst_type**, **inst_type_all**, **classid2entid**, **subclassof2id**, **subclassof_all2id**, **rid2domid**, **rid2rangeid**) that are stored as lists are converted to sets, only when it is lossless (no duplicates and only int elements). In the original datasets, this concerns **classid2entid** in all datasets and **subclassof_all2id** in DB100k+
   * In NELL-995+, entities, relations and classes do not have valid IRIs (e.g., ``concept:city:paris``, or coordinates such as ``48.59,-53.73``). They are prefixed with ``http://nell.example.org/`` (e.g., ``http://nell.example.org/concept:city:paris``) in **ent2id**, **rel2id** and **class2id**
   * Dataset splits and other pickles are copied unchanged
   * See the ``dataset_cleaning.py`` Python script that performs this cleaning procedure
   * See [``dataset_cleaning_all.sh``](dataset_cleaning_all.sh)
   * See folders ``cleaned-dataset/``
3. Reconstruct the datasets from the cleaned datasets
   * Full dataset merging train/val/test sets and TBox axioms
   * Only train set + TBox axioms
   * Only train set + val set + TBox axioms
   * See the ``dataset_reconstruct.py`` Python script that groups all triples from the train/val (optional)/test (optional) splits and the TBox axioms
   * See [``dataset_reconstruct_all.sh``](dataset_reconstruct_all.sh)
   * See folders ``reconstructed-datasets/``
4. Use [QSE](https://github.com/dkw-aau/qse) to mine SHACL shapes from the full datasets
   * Using a confidence of 0.8 and a support of 100
   * Using a fixed version of QSE from the Wimmics team (provided by [Camille Juigné](https://cjuigne.github.io/cjuigne/)), not yet publicly available, vendored as [``vendor/qse-wimmics.jar``](vendor/qse-wimmics.jar) (QSE is distributed under the MIT license)
   * See the configuration files ``qse-shapes/qse_config.properties`` (one per dataset)
   * See [``qse_mine_all.sh``](qse_mine_all.sh)
   * See folders ``qse-shapes/``
5. Compute statistics on the mined shapes
   * See the ``shapes_statistics.py`` Python script to get statistics about the mined SHACL shapes 
   * See [``qse_shapes_statistics_all.sh``](qse_shapes_statistics_all.sh)
   * See folders ``qse-shapes/``
6. Clean shapes by removing those involving ``rdf:type`` paths (and iteratively, those that are empty after that)
    * See the ``shapes_cleaning.py`` Python script that performs this cleaning procedure
    * See [``qse_shapes_cleaning_all.sh``](qse_shapes_cleaning_all.sh)
    * See folders ``cleaned-shapes/``
7. Compute statistics on the mined shapes
    * See the ``shapes_statistics.py`` Python script to get statistics about the cleaned SHACL shapes 
    * See [``cleaned_shapes_statistics_all.sh``](cleaned_shapes_statistics_all.sh)
    * See folders ``cleaned-shapes/``
8. Compute validation reports on full datasets, train+TBox, and train+val+TBox datasets
    * See the ``validate_graph.py`` Python script to compute validation reports on the datasets
    * Take into account that it generates two validation reports: one with safe IRIs, and one with original IRIs (especially useful for the YAGO3-10+ dataset that contains ``"`` in IRIs)
    * See [``validate_graph_all.sh``](validate_graph_all.sh)
9. Compute validation reports statistics on full datasets, train+TBox, train+val+TBox datasets and extract the non-conformant nodes for each dataset
    * See the ``validation_reports_statistics.py`` Python script to get statistics about the validation reports 
    * See [``validation_reports_statistics_all.sh``](validation_reports_statistics_all.sh)``
    * For YAGO3-10+, it is necessary to use safe IRIs to compute the statistics

## Requirements

* Python 3.13
* [requirements.txt](requirements.txt)
* Java 21 (to run QSE)

## References

1. <span id=ref-1>Nicolas Robert, Pierre Monnin, Catherine Faron. Semantically Enriched Datasets for Link Prediction:
DB100k+, NELL-995+ and YAGO3-10+. 1st International Workshop on Advanced Neuro-Symbolic
Applications Co-located with ECAI 2025, Oct 2025, Bologna, Italy. [[paper]](https://hal.science/hal-05291884v1)</span>
2. <span id=ref-2>Kashif Rabbani, Matteo Lissandrini, Katja Hose. Extraction of Validating Shapes from very large 
Knowledge Graphs. Proc. VLDB Endow. 16(5): 1023-1032 (2023). [[paper]](https://www.vldb.org/pvldb/vol16/p1023-rabbani.pdf)</span>

## Funding acknowledgement

These datasets are part of the [SHACKLE project](https://pmonnin.github.io/shackle.html) that has received funding from the European Union, via the oc2-2024-TES-02 call issued and implemented by the ENFIELD project, under the grant agreement No 101120657. 