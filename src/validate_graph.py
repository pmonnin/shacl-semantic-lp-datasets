import argparse
import logging
import pyshacl
import rdflib
import tqdm
import urllib.parse

from utils.logging_utils import get_logger

RFC3987_SAFE_CHARS = ":/?#[]@!$&'()*+,;=%"


def encode_iri(iri: str) -> str:
    return urllib.parse.quote(iri, safe=RFC3987_SAFE_CHARS)


def is_safe_iri(iri: str) -> bool:
    return iri == encode_iri(iri)


def build_safe_graph(g: rdflib.Graph, logger: logging.Logger) -> tuple[rdflib.Graph, dict[str, str]]:
    safe_graph = rdflib.Graph()
    uri_map = {}
    seen_uris = set()

    for s, p, o in tqdm.tqdm(g):
        safe_s = encode_iri(str(s))
        uri_map[str(s)] = safe_s

        if not is_safe_iri(str(s)) and str(s) not in seen_uris:
            logger.warning(f"⚠️ Invalid IRI detected: {str(s)}")
            seen_uris.add(str(s))

        safe_o = encode_iri(str(o))
        uri_map[str(o)] = safe_o

        if not is_safe_iri(str(o)) and str(o) not in seen_uris:
            logger.warning(f"⚠️ Invalid IRI detected: {str(o)}")
            seen_uris.add(str(o))

        safe_graph.add((rdflib.URIRef(safe_s), p, rdflib.URIRef(safe_o)))

    if len(seen_uris) > 0:
        logger.warning(f"⚠️ There were {len(seen_uris)} invalid IRIs detected")

    return safe_graph, uri_map


def remap_validation_report(report: rdflib.Graph, uri_reverse_map: dict[str, str]) -> rdflib.Graph:
    remapped_report = rdflib.Graph()

    for s, p, o in report:
        if isinstance(s, rdflib.URIRef):
            s = rdflib.URIRef(uri_reverse_map.get(str(s), str(s)))

        if isinstance(o, rdflib.URIRef):
            o = rdflib.URIRef(uri_reverse_map.get(str(o), str(o)))

        remapped_report.add((s, p, o))

    return remapped_report


def main():
    parser = argparse.ArgumentParser(prog="validate_graph", description="Perform SHACL validation on RDF graph")
    parser.add_argument("--graph", dest="graph_file", help="RDF graph to validate (TTL file)", required=True)
    parser.add_argument("--shapes", dest="shapes_file", help="SHACL shapes (TTL file)", required=True)
    parser.add_argument("--output-safe-iris", dest="output_safe_iris", help="Output validation report file w/ safe IRIs",required=True)
    parser.add_argument("--output-original-iris", dest="output_original_iris", help="Output validation report file w/ original IRIs", required=True)
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
    safe_graph, uri_map = build_safe_graph(graph, logger)

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
    logger.info(f"Save validation report w/ safe IRIs to {args.output_safe_iris}")
    results_graph.serialize(destination=args.output_safe_iris, format="turtle")

    # Save validation report w/ original IRIs
    logger.info(f"Save validation report w/ original IRIs to {args.output_original_iris}")
    with open(args.output_safe_iris, "r", encoding="utf-8") as f:
        safe_report = f.read()

    for iri, mapped_iri in uri_map.items():
        safe_report = safe_report.replace(mapped_iri, iri)

    with open(args.output_original_iris, "w", encoding="utf-8") as f:
        f.write(safe_report)

    logger.info("validate_graph: end")


if __name__ == '__main__':
    main()
