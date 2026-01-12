import argparse
import csv
import pickle
import tqdm

from utils.logging_utils import get_logger


def load_mapping(file_path: str) -> dict[str, int]:
    return pickle.load(open(file_path, "rb"))


def reverse_mapping(mapping: dict[str, int]) -> dict[int, str]:
    inv_mapping = {}
    for k, v in mapping.items():
        inv_mapping[v] = k
    return inv_mapping

def load_convert_triples(file_path: str, id2ent: dict[int, str], id2rel: dict[int, str]) -> list[tuple[str, str, str]]:
    triples = []
    with open(file_path, "r") as f:
        csvreader = csv.reader(f, delimiter="\t")
        for r in tqdm.tqdm(csvreader):
            triples.append((id2ent[int(r[0])], id2rel[int(r[1])], id2ent[int(r[2])]))
    return triples


def load_convert_type_triples(file_path: str, id2ent: dict[int, str], id2class: dict[int, str]) -> list[tuple[str, str, str]]:
    triples = []
    axioms = pickle.load(open(file_path, "rb"))
    for k, v in tqdm.tqdm(axioms.items()):
        for v2 in v:
            triples.append((id2ent[k], "<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>", id2class[v2]))
    return triples


def load_convert_subclass_triples(file_path: str, id2class: dict[int, str]) -> list[tuple[str, str, str]]:
    triples = []
    axioms = pickle.load(open(file_path, "rb"))
    for k, v in tqdm.tqdm(axioms.items()):
        for v2 in v:
            triples.append((id2class[k], "<http://www.w3.org/2000/01/rdf-schema#subClassOf>", id2class[v2]))
    return triples


def load_convert_relation_schema_triples(file_path: str, id2rel: dict[int, str], id2class: dict[int, str], axiom_type: str) -> list[tuple[str, str, str]]:
    triples = []
    axioms = pickle.load(open(file_path, "rb"))
    for k, v in tqdm.tqdm(axioms.items()):
        for v2 in v:
            triples.append((id2rel[k], f"<http://www.w3.org/2000/01/rdf-schema#{axiom_type}>", id2class[v2]))
    return triples


def clean_uri(uri: str) -> str:
    if not uri.startswith("<"):
        uri = f"<{uri}"
    if not uri.endswith(">"):
        uri = f"{uri}>"
    return uri


def clean_triples(triples: list[tuple[str, str, str]]):
    cleaned_triples = []
    for t in tqdm.tqdm(triples):
        cleaned_triples.append((clean_uri(t[0]), clean_uri(t[1]), clean_uri(t[2])))
    return cleaned_triples


def main():
    parser = argparse.ArgumentParser(prog="dataset_reconstruct", description="Reconstruct full dataset from t"
                                                                             "rain/val/test splits and rdf:type and "
                                                                             "rdfs:sublassOf triples")
    parser.add_argument("--train-triples", dest="train_triples", help="Train triples file", required=True)
    parser.add_argument("--val-triples", dest="val_triples", help="Validation triples file", required=False)
    parser.add_argument("--test-triples", dest="test_triples", help="Test triples file", required=False)
    parser.add_argument("--inst-triples", dest="inst_triples", help="rdf:type triples file", required=True)
    parser.add_argument("--sub-triples", dest="sub_triples", help="rdfs:subClassOf triples file", required=True)
    parser.add_argument("--r2domid", dest="r2domid", help="Relation to domain ID file", required=True)
    parser.add_argument("--r2rangeid", dest="r2rangeid", help="Relation to range ID file", required=True)
    parser.add_argument("--ent2id", dest="ent2id", help="Entity to ID file", required=True)
    parser.add_argument("--rel2id", dest="rel2id", help="Relation to ID file", required=True)
    parser.add_argument("--class2id", dest="class2id", help="Class to ID file", required=True)
    parser.add_argument("--output", dest="output", help="Output file", required=True)
    parser.add_argument("-l,--log-level", dest="log_level", help="Set the logging level", type=str,
                        default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    args = parser.parse_args()

    logger = get_logger(args.log_level)

    logger.info("dataset_reconstruct: start")

    # Load entity -> id mapping and reverse it
    logger.info("Load entity -> id mapping")
    ent2id = load_mapping(args.ent2id)
    id2ent = reverse_mapping(ent2id)

    # Load relation -> id mapping and reverse it
    logger.info("Load relation -> id mapping")
    rel2id = load_mapping(args.rel2id)
    id2rel = reverse_mapping(rel2id)

    # Load class -> id mapping and reverse it
    logger.info("Load class -> id mapping")
    class2id = load_mapping(args.class2id)
    id2class = reverse_mapping(class2id)

    # Load train triples and convert
    logger.info("Load and convert train triples")
    train_triples = load_convert_triples(args.train_triples, id2ent, id2rel)

    # Load val triples and convert
    logger.info("Load and convert val triples")
    val_triples = []
    if args.val_triples:
        val_triples = load_convert_triples(args.val_triples, id2ent, id2rel)

    # Load test triples and convert
    logger.info("Load and convert test triples")
    test_triples = []
    if args.test_triples:
        test_triples = load_convert_triples(args.test_triples, id2ent, id2rel)

    # Load rdf:type triples and convert
    logger.info("Load and convert rdf:type triples")
    type_triples = load_convert_type_triples(args.inst_triples, id2ent, id2class)

    # Load rdfs:subClassOf triples and convert
    logger.info("Load and convert rdfs:subClassOf triples")
    sub_triples = load_convert_subclass_triples(args.sub_triples, id2class)

    # Load rdfs:domain triples and convert
    logger.info("Load and convert rdfs:domain triples")
    domain_triples = load_convert_relation_schema_triples(args.r2domid, id2rel, id2class, "domain")

    # Load rdfs:range triples and convert
    logger.info("Load and convert rdfs:range triples")
    range_triples = load_convert_relation_schema_triples(args.r2rangeid, id2rel, id2class, "range")

    # Compute full triples
    full_triples = train_triples + val_triples + test_triples + type_triples + sub_triples + domain_triples + range_triples
    logger.info(f"Total number of triples: {len(full_triples)}")

    # Clean triples (update malformed entities)
    logger.info("Clean triples")
    cleaned_triples = clean_triples(full_triples)

    # Save cleaned triples
    logger.info(f"Save cleaned triples to {args.output}")
    with open(args.output, "w") as f:
        for t in cleaned_triples:
            f.write(f"{t[0]}\t{t[1]}\t{t[2]} .\n")

    logger.info("dataset_reconstruct: done")


if __name__ == '__main__':
    main()
