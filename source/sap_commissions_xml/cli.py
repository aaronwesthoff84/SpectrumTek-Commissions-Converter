from __future__ import annotations

import argparse
from pathlib import Path
from xml.etree.ElementTree import ParseError

from .parser import SAPCommissionsXMLParser
from .writer import SHEET_COLUMNS, write_csv_outputs, write_xlsx_output


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Parse SAP Commissions XML into tabular outputs equivalent to the VBA workbook."
    )
    parser.add_argument("input", help="Path to SAP Commissions XML export")
    parser.add_argument(
        "-o",
        "--output",
        default="parsed_plan.xlsx",
        help="Output file or directory. Use .xlsx for workbook output or a directory for CSV output.",
    )
    parser.add_argument(
        "--format",
        choices=["xlsx", "csv", "auto"],
        default="auto",
        help="Output format. 'auto' infers from --output extension.",
    )
    return parser


def main() -> int:
    args = build_arg_parser().parse_args()

    parser = SAPCommissionsXMLParser()
    try:
        result = parser.parse_file(args.input)
    except FileNotFoundError as exc:
        print(f"Error: {exc}")
        return 2
    except ParseError as exc:
        print(f"Error: invalid XML - {exc}")
        return 2

    output_path = Path(args.output)
    output_format = args.format
    if output_format == "auto":
        output_format = "xlsx" if output_path.suffix.lower() == ".xlsx" else "csv"

    try:
        if output_format == "xlsx":
            written_to = write_xlsx_output(result.rows, output_path)
        else:
            written_to = write_csv_outputs(result.rows, output_path)
    except RuntimeError as exc:
        print(f"Error: {exc}")
        if output_format == "xlsx":
            print("Tip: install dependencies with `pip install -r requirements.txt` or use `--format csv`.")
        return 2

    print(f"Parsed: {args.input}")
    print(f"Output ({output_format}): {written_to}")

    for sheet_name in SHEET_COLUMNS:
        print(f"- {sheet_name}: {len(result.rows.get(sheet_name, []))} rows")

    print(f"Warnings: {result.logger.count_warnings()}")
    print(f"Errors: {result.logger.count_errors()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
