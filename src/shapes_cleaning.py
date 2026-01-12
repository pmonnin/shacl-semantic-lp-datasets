import argparse
import rdflib
import tqdm

from utils.logging_utils import get_logger
from utils.shacl_utils import SH


NODE_CONSTRAINT_PREDICATES = {
    SH.property,
    SH.node,
    SH["and"],
    SH["or"],
    SH["not"],
    SH.xone,
    SH["class"],
    SH.datatype,
    SH.minCount,
    SH.maxCount,
    SH.pattern,
    SH["in"],
    SH.qualifiedValueShape,
    SH.closed,
    SH.ignoredProperties,
}


def main():
    parser = argparse.ArgumentParser(prog="shapes_cleaning", description="Removes rdf:type path constraints from shapes")
    parser.add_argument("--shapes", dest="shapes_file", help="SHACL shapes file", required=True)
    parser.add_argument("--output", dest="output", help="Output file", required=True)
    parser.add_argument("-l,--log-level", dest="log_level", help="Set the logging level", type=str,
                        default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    args = parser.parse_args()

    logger = get_logger(args.log_level)

    logger.info("shapes_cleaning: start")

    logger.info("Load shapes")
    g = rdflib.Graph().parse(args.shapes_file)

    # Detect shapes to remove
    logger.info("Detect PropertyShapes to fully remove or remove sh:path rdf:type constraint when multiple paths are present")
    shapes_to_remove = set()
    for ps in tqdm.tqdm(g.subjects(rdflib.RDF.type, SH.PropertyShape)):
        has_path_rdf_type = False
        has_other_path = False

        for p, s in g.predicate_objects(ps):
            if p == SH.path and s == rdflib.RDF.type:
                has_path_rdf_type = True
            if p == SH.path and s != rdflib.RDF.type:
                has_other_path = True

        if has_path_rdf_type:
            if not has_other_path:
                shapes_to_remove.add(ps)
            else:
                # If there are other paths, just remove rdf:type path constraint
                g.remove((ps, SH.path, rdflib.RDF.type))

    # Remove shapes that only have rdf:type path constraint
    logger.info("Remove rdf:type path constraints from shapes, associated empty PropertyShapes and blank nodes")
    for ps in tqdm.tqdm(shapes_to_remove):
        triples_to_remove = set()

        triples_to_remove |= set(g.triples((None, None, ps)))
        triples_to_remove |= set(g.triples((ps, None, None)))

        # Removing associated blank nodes with transitive closure
        stack = [ps]
        seen = {ps}
        while stack:
            current = stack.pop()
            for s, p, o in list(g.triples((current, None, None))):
                triples_to_remove.add((s, p, o))
                if isinstance(o, rdflib.BNode) and o not in seen:
                    stack.append(o)
                    seen.add(o)

        for t in triples_to_remove:
            g.remove(t)

        assert not list(g.triples((ps, None, None)))
        assert not list(g.triples((None, None, ps)))

    # Clean empty NodeShapes
    logger.info("Clean empty NodeShapes")
    for ns in tqdm.tqdm(g.subjects(rdflib.RDF.type, SH.NodeShape)):
        has_constraints = False

        for _, p, _ in g.triples((ns, None, None)):
            if p in NODE_CONSTRAINT_PREDICATES:
                has_constraints = True

        if not has_constraints:
            g.remove((ns, None, None))
            g.remove((None, None, ns))


    logger.info(f"Write cleaned shapes to {args.output}")
    g.serialize(destination=args.output, format="turtle")

    logger.info("shapes_cleaning: done")


if __name__ == '__main__':
    main()
