import argparse
import logging
import pickle
import pyshacl
import rdflib
import tqdm
import urllib.parse

from utils.logging_utils import get_logger

RFC3987_SAFE_CHARS = ":/?#[]@!$&'()*+,;=%"


def encode_iri(iri: str) -> str:
    return urllib.parse.quote(iri, safe=RFC3987_SAFE_CHARS)


def build_safe_graph(g: rdflib.Graph, logger: logging.Logger) -> tuple[rdflib.Graph, dict[str, str]]:
    safe_graph = rdflib.Graph()
    iri_map = {}

    for s, p, o in tqdm.tqdm(g):
        safe_s = encode_iri(str(s))

        if safe_s != str(s) and str(s) not in iri_map:
            logger.warning(f"⚠️ Invalid IRI detected: {str(s)}")
            iri_map[str(s)] = safe_s

        safe_o = encode_iri(str(o))

        if safe_o != str(o) and str(o) not in iri_map:
            logger.warning(f"⚠️ Invalid IRI detected: {str(o)}")
            iri_map[str(o)] = safe_o

        safe_graph.add((rdflib.URIRef(safe_s), p, rdflib.URIRef(safe_o)))

    if len(iri_map) > 0:
        logger.warning(f"⚠️ There were {len(iri_map)} invalid IRIs detected")

    return safe_graph, iri_map


def main():
    parser = argparse.ArgumentParser(prog="validate_graph", description="Perform SHACL validation on RDF graph")
    parser.add_argument("--graph", dest="graph_file", help="RDF graph to validate (TTL file)", required=True)
    parser.add_argument("--shapes", dest="shapes_file", help="SHACL shapes (TTL file)", required=True)
    parser.add_argument("--output", dest="output", help="Output validation report file (w/ safe IRIs)", required=True)
    parser.add_argument("--output-iri-map", dest="output_iri_map", help="Output pickle file mapping each IRI that was "
                                                                        "encoded to its safe IRI", required=False)
    parser.add_argument("-l,--log-level", dest="log_level", help="Set the logging level", type=str,
                        default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    args = parser.parse_args()

    logger = get_logger(args.log_level)

    logger.info("validate_graph: start")

    # Load RDF graph
    logger.info(f"Load RDF graph from {args.graph_file}")
    graph = rdflib.Graph().parse(args.graph_file)

    # Load SHACL shapes
    logger.info(f"Load SHACL shapes from {args.shapes_file}")
    shapes = rdflib.Graph().parse(args.shapes_file)

    # Build safe graph before validation (detect invalid IRIs)
    logger.info("Build safe graph before validation by detecting and encoding invalid IRIs")
    safe_graph, iri_map = build_safe_graph(graph, logger)

    # Save the map of encoded IRIs
    if args.output_iri_map:
        logger.info(f"Save the {len(iri_map)} encoded IRIs to {args.output_iri_map}")
        pickle.dump(iri_map, open(args.output_iri_map, "wb"))

    # Validate graph
    logger.info("Validate safe RDF graph")
    conforms, results_graph, results_text  = pyshacl.validate(
        safe_graph,
        shacl_graph=shapes,
        inference='none',
        abort_on_first=False,
        allow_infos=False,
        allow_warnings=False,
        meta_shacl=False,
        advanced=False,
        js=False,
        debug=False
    )

    if conforms:
        logger.info("✅ Graph conforms to SHACL shapes")

    else:
        logger.info("🔴 Graph does not conform to SHACL shapes")

    # Save validation report w/ safe IRIs
    logger.info(f"Save validation report w/ safe IRIs to {args.output}")
    results_graph.serialize(destination=args.output, format="turtle")

    logger.info("validate_graph: end")


if __name__ == '__main__':
    main()
