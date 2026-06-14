from __future__ import annotations

import json
import logging
from decimal import Decimal
from pathlib import Path
from typing import Iterable, Union, Any

try:
    import ijson
    HAS_IJSON = True
except ImportError:
    HAS_IJSON = False


logger = logging.getLogger(__name__)


class _JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


def _ensure_iterable(data: Any) -> Iterable[dict]:
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        return [data]
    raise ValueError("JSON root must be a dict or list of dicts")


def _validate_record(record: Any) -> dict:
    if not isinstance(record, dict):
        raise ValueError(f"Invalid record type: {type(record)}. Expected dict.")
    return record


def convert_json_to_jsonl(
    input_path: Union[str, Path],
    output_path: Union[str, Path],
) -> None:
    input_path = Path(input_path)
    output_path = Path(output_path)

    logger.info(f"Reading JSON from {input_path}")

    with input_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    records = _ensure_iterable(data)

    logger.info(f"Writing JSONL to {output_path}")

    with output_path.open("w", encoding="utf-8") as f:
        for record in records:
            record = _validate_record(record)
            f.write(json.dumps(record, ensure_ascii=False, cls=_JsonEncoder) + "\n")

    logger.info("Conversion completed (standard mode)")


def convert_large_json_array_to_jsonl(
    input_path: Union[str, Path],
    output_path: Union[str, Path],
) -> None:
    if not HAS_IJSON:
        raise RuntimeError(
            "ijson is required for streaming mode. Install with: pip install ijson"
        )

    input_path = Path(input_path)
    output_path = Path(output_path)

    logger.info(f"Streaming JSON from {input_path}")

    with input_path.open("r", encoding="utf-8") as f_in, \
         output_path.open("w", encoding="utf-8") as f_out:

        count = 0
        for item in ijson.items(f_in, "item"):
            item = _validate_record(item)
            f_out.write(json.dumps(item, ensure_ascii=False, cls=_JsonEncoder) + "\n")
            count += 1

    logger.info(f"Conversion completed (stream mode) - {count} records written")


def convert(
    input_path: Union[str, Path],
    output_path: Union[str, Path],
    streaming: bool = False,
) -> None:
    if streaming:
        convert_large_json_array_to_jsonl(input_path, output_path)
    else:
        convert_json_to_jsonl(input_path, output_path)


def _build_parser():
    import argparse

    parser = argparse.ArgumentParser(
        description="Convert JSON to JSONL"
    )

    parser.add_argument(
        "input",
        type=str,
        help="Path to input JSON file"
    )

    parser.add_argument(
        "output",
        type=str,
        help="Path to output JSONL file"
    )

    parser.add_argument(
        "--stream",
        action="store_true",
        help="Enable streaming mode (for large JSON arrays)"
    )

    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        help="Logging level (DEBUG, INFO, WARNING, ERROR)"
    )

    return parser


def _setup_logging(level: str):
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )


def main():
    parser = _build_parser()
    args = parser.parse_args()

    _setup_logging(args.log_level)

    try:
        convert(
            input_path=args.input,
            output_path=args.output,
            streaming=args.stream,
        )
    except Exception as e:
        logger.exception(f"Conversion failed: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()