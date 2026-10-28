import argparse
import logging
import pathlib
import pickle
import shutil
import tqdm

from utils.logging_utils import get_logger

# Pickles mapping an id to a set of ids
SET_MAPPING_FILES = [
    "inst_type.pkl",
    "inst_type_all.pkl",
    "classid2entid.pkl",
    "subclassof2id.pkl",
    "subclassof_all2id.pkl",
    "rid2domid.pkl",
    "rid2rangeid.pkl",
]

# Pickles mapping an IRI to an id
IRI_MAPPING_FILES = [
    "ent2id.pkl",
    "rel2id.pkl",
    "class2id.pkl",
]


def fix_set_mapping(mapping: dict[int, set[int] | list], file_name: str,
                    logger: logging.Logger) -> dict[int, set[int] | list]:
    """
    Convert list values to sets in place, only when it is lossless (no duplicates and only int elements).
    Other list values are kept and reported for manual inspection.
    :param mapping: mapping from an id to a set or a list of ids, modified in place
    :param file_name: name of the pickle file the mapping comes from, used in log messages
    :param logger: logger used to report conversions and list values left unconverted
    :return: the same mapping object, whose list values are sets except the ones that could not be converted
    """
    fixed_keys = []
    unsafe_keys = []

    for k, v in tqdm.tqdm(mapping.items()):
        if type(v) != list:
            continue
        if len(v) != len(set(v)) or any(type(e) != int for e in v):
            unsafe_keys.append(k)
            continue
        mapping[k] = set(v)
        fixed_keys.append(k)

    if unsafe_keys:
        logger.error(f"{file_name}: {len(unsafe_keys)} list values NOT converted (duplicates or non-int elements), "
                     f"e.g. keys {unsafe_keys[:5]}")

    logger.info(f"{file_name}: converted {len(fixed_keys)}/{len(mapping)} list values to sets")
    return mapping


def prefix_iri_mapping(mapping: dict[str, int], file_name: str, iri_prefix: str, logger: logging.Logger) -> dict[str, int]:
    """
    Prefix every IRI with iri_prefix (IRIs already starting with it are left untouched). The input mapping is not
    modified.
    :param mapping: mapping from an IRI to an id
    :param file_name: name of the pickle file the mapping comes from, used in log messages
    :param iri_prefix: prefix added in front of each IRI
    :param logger: logger used to report the number of prefixed IRIs
    :return: a new mapping from the prefixed IRIs to the same ids
    """
    prefixed_mapping = {}
    prefixed_count = 0

    for k, v in tqdm.tqdm(mapping.items()):
        if not k.startswith(iri_prefix):
            k = f"{iri_prefix}{k}"
            prefixed_count += 1
        prefixed_mapping[k] = v

    assert len(prefixed_mapping) == len(mapping)

    logger.info(f"{file_name}: prefixed {prefixed_count}/{len(mapping)} IRIs with {iri_prefix}")
    return prefixed_mapping


def main():
    parser = argparse.ArgumentParser(prog="dataset_cleaning", description="Clean an original dataset: convert list "
                                                                          "values of mapping pickles to sets and "
                                                                          "optionally prefix IRIs")
    parser.add_argument("--input-dir", dest="input_dir", help="Original dataset folder", required=True)
    parser.add_argument("--output-dir", dest="output_dir", help="Cleaned dataset folder", required=True)
    parser.add_argument("--iri-prefix", dest="iri_prefix", help="Prefix added to entity, relation and class IRIs",
                        required=False)
    parser.add_argument("-l,--log-level", dest="log_level", help="Set the logging level", type=str,
                        default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    args = parser.parse_args()

    logger = get_logger(args.log_level)

    logger.info("dataset_cleaning: start")

    input_dir = pathlib.Path(args.input_dir)
    output_dir = pathlib.Path(args.output_dir)
    (output_dir / "pickle").mkdir(parents=True, exist_ok=True)

    # Copy dataset splits unchanged
    logger.info(f"Copy dataset splits to {output_dir}")
    for f in sorted(input_dir.glob("*.txt")):
        shutil.copy2(f, output_dir / f.name)

    # Clean pickles
    for f in sorted((input_dir / "pickle").glob("*.pkl")):
        if f.name in SET_MAPPING_FILES:
            logger.info(f"Convert list values to sets in {f.name}")
            mapping = fix_set_mapping(pickle.load(open(f, "rb")), f.name, logger)
            pickle.dump(mapping, open(output_dir / "pickle" / f.name, "wb"))

        elif f.name in IRI_MAPPING_FILES and args.iri_prefix:
            logger.info(f"Prefix IRIs in {f.name}")
            mapping = prefix_iri_mapping(pickle.load(open(f, "rb")), f.name, args.iri_prefix, logger)
            pickle.dump(mapping, open(output_dir / "pickle" / f.name, "wb"))

        else:
            logger.info(f"Copy {f.name} unchanged")
            shutil.copy2(f, output_dir / "pickle" / f.name)

    logger.info("dataset_cleaning: done")


if __name__ == '__main__':
    main()
