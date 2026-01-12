import argparse
import collections
import rdflib

from utils.logging_utils import get_logger
from utils.shacl_utils import SH

NODE_SHAPES_EXCLUDED_PROPERTIES = {
    rdflib.RDF.type,
    SH.targetClass,
    SH.targetNode,
    SH.targetSubjectsOf,
    SH.targetObjectsOf,
    SH.property,
    SH.node,
    SH.message,
    SH.severity,
    SH.description,
    SH.name,
    SH.deactivated,
}


PROPERTY_SHAPE_EXCLUDED_PROPERTIES = {
    rdflib.RDF.type,
    SH.path,
    SH.property,
    SH.node,
    SH.qualifiedValueShape,
    SH.qualifiedMinCount,
    SH.qualifiedMaxCount,
    SH.targetClass,
    SH.targetNode,
    SH.targetSubjectsOf,
    SH.targetObjectsOf,
    SH.group,
    SH.order,
    SH.name,
    SH.description,
    SH.message,
    SH.severity,
    SH.deactivated,
}


def get_shapes(graph):
    node_shapes = set(graph.subjects(rdflib.RDF.type, SH.NodeShape))
    property_shapes = set(graph.subjects(rdflib.RDF.type, SH.PropertyShape))
    all_shapes = node_shapes | property_shapes
    return all_shapes, node_shapes, property_shapes


def get_avg_property_shapes(graph, node_shapes):
    counts = []

    for ns in node_shapes:
        counts.append(len(list(graph.objects(ns, SH.property))))

    if not counts:
        return 0.0

    return sum(counts) / len(counts)


def get_number_of_paths(graph):
    return len(list(graph.triples((None, SH.path, None))))


def get_number_rdf_type_paths(graph):
    return len(list(graph.triples((None, SH.path, rdflib.RDF.type))))


def list_shape_constraints(graph, shapes, excluded_properties):
    counter = collections.Counter()

    for s in shapes:
        for p, _ in graph.predicate_objects(s):
            if isinstance(p, rdflib.URIRef) and p.startswith(str(SH)) and p not in excluded_properties:
                counter[p] += 1

    return counter


def main():
    parser = argparse.ArgumentParser(prog="shapes_statistics", description="Compute statistics on the input shapes")
    parser.add_argument("--shapes", dest="shapes_file", help="SHACL shapes file", required=True)
    parser.add_argument("--output", dest="output", help="Output file", required=True)
    parser.add_argument("-l,--log-level", dest="log_level", help="Set the logging level", type=str,
                        default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    args = parser.parse_args()

    logger = get_logger(args.log_level)

    logger.info("shapes_statistics: start")

    logger.info("Load shapes")
    g = rdflib.Graph().parse(args.shapes_file)

    logger.info(f"Compute and write statistics to {args.output}")
    with open(args.output, "w") as f:
        f.write(f"# SHACL shapes statistics:\n")

        f.write(f"\n## File statistics\n")
        f.write(f"* Number of triples: {len(g)}\n")

        all_shapes, node_shapes, property_shapes = get_shapes(g)
        f.write(f"\n## Shapes statistics\n")
        f.write(f"* Total shapes: {len(all_shapes)}\n")
        f.write(f"* NodeShapes: {len(node_shapes)}\n")
        f.write(f"* PropertyShapes: {len(property_shapes)}\n")
        f.write(f"* Average number of properties per NodeShape: {get_avg_property_shapes(g, node_shapes)}\n")

        f.write("\n## Details on NodeShapes constraints\n")
        f.write(f"* List of constraints (top-level, not nested):\n")
        for p, c in list_shape_constraints(g, node_shapes, NODE_SHAPES_EXCLUDED_PROPERTIES).items():
            f.write(f"  * {p}: {c}\n")

        f.write("\n## Details on PropertyShapes constraints\n")
        f.write(f"* List of constraints (top-level, not nested):\n")
        for p, c in list_shape_constraints(g, property_shapes, PROPERTY_SHAPE_EXCLUDED_PROPERTIES).items():
            f.write(f"  * {p}: {c}\n")

        f.write("* Details on paths\n")
        total_paths = get_number_of_paths(g)
        type_paths = get_number_rdf_type_paths(g)
        f.write(f"  * Number of paths: {total_paths}\n")
        f.write(f"  * Number of rdf:type paths: {type_paths} ({(type_paths / total_paths * 100):.2f} %)\n")
        f.write(f"  * Number of other paths: {total_paths - type_paths} ({((total_paths - type_paths) / total_paths * 100):.2f} %)\n")

    logger.info("shapes_statistics: done")


if __name__ == '__main__':
    main()
