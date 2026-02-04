import argparse
import rdflib

from utils.logging_utils import get_logger


def main():
    parser = argparse.ArgumentParser(prog="validation_reports_statistics", description="Compute statistics on the validation reports for full and train datasets")
    parser.add_argument("--report-full", dest="report_full_file", help="Validation report file on full dataset", required=True)
    parser.add_argument("--report-train", dest="report_train_file", help="Validation report file on train dataset", required=True)
    parser.add_argument("--output", dest="output", help="Output file", required=True)
    parser.add_argument("-l,--log-level", dest="log_level", help="Set the logging level", type=str,
                        default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    args = parser.parse_args()

    logger = get_logger(args.log_level)

    logger.info("validation_report_statistics: start")

    logger.info("Load validation report for the full dataset")
    report_full_graph = rdflib.Graph().parse(args.report_full_file)

    logger.info("Load validation report for the train dataset")
    report_train_graph = rdflib.Graph().parse(args.report_train_file)

    # Compute non-conformant nodes
    logger.info("Compute non-conformant nodes")

    non_conformant_nodes_query = """
        PREFIX sh: <http://www.w3.org/ns/shacl#>

        SELECT DISTINCT ?node
        WHERE {
            ?report a sh:ValidationReport ;
                    sh:result ?result .
            ?result sh:focusNode ?node .
        }
    """

    full_non_conformant_nodes = {row["node"] for row in report_full_graph.query(non_conformant_nodes_query)}
    train_non_conformant_nodes = {row["node"] for row in report_train_graph.query(non_conformant_nodes_query)}

    logger.info("Compute and write statistics")
    with open(args.output, "w") as f:
        f.write("# Validation report statistics\n")
        f.write(f"* Full dataset non-conformant nodes: {len(full_non_conformant_nodes)}\n")
        f.write(f"* Train dataset non-conformant nodes: {len(train_non_conformant_nodes)}\n")

        train_fixed_nodes = train_non_conformant_nodes - full_non_conformant_nodes
        f.write(f"* Train un-conformant nodes that are conformant in full (and still validated): {len(train_fixed_nodes)}")

    logger.info("validation_reports_statistics: done")


if __name__ == '__main__':
    main()
