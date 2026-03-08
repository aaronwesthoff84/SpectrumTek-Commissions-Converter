from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class Column:
    key: str
    header: str


def _metric_columns() -> list[Column]:
    cols: list[Column] = []
    cols.extend([Column(f"GA{i}", f"GA{i}") for i in range(1, 17)])
    cols.extend([Column(f"GN{i}", f"GN{i}") for i in range(1, 7)])
    cols.extend([Column(f"GD{i}", f"GD{i}") for i in range(1, 7)])
    cols.extend([Column(f"GB{i}", f"GB{i}") for i in range(1, 7)])
    return cols


SHEET_COLUMNS: dict[str, list[Column]] = {
    "PLANS": [
        Column("CALENDAR", "Calendar"),
        Column("NAME", "Name"),
        Column("DESCRIPTION", "Description"),
        Column("EFFECTIVE_START_DATE", "Start Date"),
        Column("EFFECTIVE_END_DATE", "End Date"),
        Column("COMPONENT_NAME", "Component"),
        Column("COMPONENT_EFFECTIVE_START_DATE", "Component Start"),
        Column("COMPONENT_EFFECTIVE_END_DATE", "Component End"),
    ],
    "COMPONENTS": [
        Column("CALENDAR", "Calendar"),
        Column("NAME", "Name"),
        Column("DESCRIPTION", "Description"),
        Column("EFFECTIVE_START_DATE", "Start Date"),
        Column("EFFECTIVE_END_DATE", "End Date"),
        Column("RULE_NAME", "Rule"),
        Column("RULE_TYPE", "Rule Type"),
        Column("RULE_EFFECTIVE_START_DATE", "Rule Start"),
        Column("RULE_EFFECTIVE_END_DATE", "Rule End"),
    ],
    "CREDITRULES": [
        Column("CALENDAR", "Calendar"),
        Column("NAME", "Name"),
        Column("DESCRIPTION", "Description"),
        Column("EFFECTIVE_START_DATE", "Start Date"),
        Column("EFFECTIVE_END_DATE", "End Date"),
        Column("CONDITION", "Condition"),
        Column("EVENT_TYPE", "Event Type"),
        Column("RULE_TYPE", "Rule Type"),
        Column("RELATION_TYPE", "Relation Type"),
        Column("OUTPUT_NAME", "Output Name"),
        Column("DISPLAY_NAME_FOR_REPORTS", "Display Name"),
        Column("IS_REPORTABLE", "Reportable"),
        Column("PERIOD_TYPE", "Period Type"),
        Column("OUTPUT_TYPE", "Type"),
        Column("UNIT_TYPE", "Unit Type"),
        Column("VALUE", "Value"),
        Column("HOLD_REF_NAME", "Hold"),
        Column("HOLD_REF_PERIOD_TYPE", "Release"),
        Column("OUTPUT_CONDITION", "Conditions"),
        Column("CREDIT_TYPE", "Credit Type"),
        Column("DUPLICATE", "Duplicate"),
        Column("ROLL_UP", "Roll Up"),
        Column("ROLL_DATE", "Roll Date"),
        *_metric_columns(),
    ],
    "MEASUREMENTS": [
        Column("CALENDAR", "Calendar"),
        Column("NAME", "Name"),
        Column("DESCRIPTION", "Description"),
        Column("EFFECTIVE_START_DATE", "Start Date"),
        Column("EFFECTIVE_END_DATE", "End Date"),
        Column("CONDITION", "Condition"),
        Column("RULE_TYPE", "Rule Type"),
        Column("OUTPUT_NAME", "Output Name"),
        Column("DISPLAY_NAME_FOR_REPORTS", "Display Name"),
        Column("IS_REPORTABLE", "Reportable"),
        Column("PERIOD_TYPE", "Period Type"),
        Column("OUTPUT_TYPE", "Type"),
        Column("UNIT_TYPE", "Unit Type"),
        Column("VALUE", "Value"),
        *_metric_columns(),
    ],
    "INCENTIVES": [
        Column("CALENDAR", "Calendar"),
        Column("NAME", "Name"),
        Column("DESCRIPTION", "Description"),
        Column("EFFECTIVE_START_DATE", "Start Date"),
        Column("EFFECTIVE_END_DATE", "End Date"),
        Column("CONDITION", "Condition"),
        Column("RULE_TYPE", "Rule Type"),
        Column("OUTPUT_NAME", "Output Name"),
        Column("DISPLAY_NAME_FOR_REPORTS", "Display Name"),
        Column("IS_REPORTABLE", "Reportable"),
        Column("PERIOD_TYPE", "Period Type"),
        Column("OUTPUT_TYPE", "Type"),
        Column("UNIT_TYPE", "Unit Type"),
        Column("VALUE", "Value"),
        Column("RATE", "Rate"),
        Column("HOLD_REF_NAME", "HOLD_REF_NAME"),
        Column("HOLD_REF_PERIOD_OFFSET", "HOLD_REF_PERIOD_OFFSET"),
        Column("HOLD_REF_PERIOD_TYPE", "HOLD_REF_PERIOD_TYPE"),
        *_metric_columns(),
    ],
    "DEPOSITS": [
        Column("CALENDAR", "Calendar"),
        Column("NAME", "Name"),
        Column("DESCRIPTION", "Description"),
        Column("EFFECTIVE_START_DATE", "Start Date"),
        Column("EFFECTIVE_END_DATE", "End Date"),
        Column("CONDITION", "Condition"),
        Column("RULE_TYPE", "Rule Type"),
        Column("OUTPUT_NAME", "Output Name"),
        Column("DISPLAY_NAME_FOR_REPORTS", "Display Name"),
        Column("IS_REPORTABLE", "Reportable"),
        Column("PERIOD_TYPE", "Period Type"),
        Column("OUTPUT_TYPE", "Type"),
        Column("UNIT_TYPE", "Unit Type"),
        Column("VALUE", "Value"),
        Column("HOLD_REF_NAME", "Hold"),
        Column("HOLD_CONDITION", "Hold Condition"),
        Column("EARNING_GROUP", "Earning Group"),
        Column("EARNING_CODE", "Earning Code"),
        *_metric_columns(),
    ],
    "LOOKUP_TABLES": [
        Column("CALENDAR", "Calendar"),
        Column("NAME", "Name"),
        Column("DESCRIPTION", "Description"),
        Column("EFFECTIVE_START_DATE", "Start Date"),
        Column("EFFECTIVE_END_DATE", "End Date"),
        Column("UNIT_TYPE", "Unit Type"),
        Column("CONVERT_NULL_VALUE", "Convert NULL"),
        Column("DIM_NAME", "Dim Name"),
        Column("DIM_EFFECTIVE_START_DATE", "Dim Start Date"),
        Column("DIM_EFFECTIVE_END_DATE", "Dim End Date"),
        Column("CASE_SENSITIVE", "Case Sensitive"),
        Column("DIM_TYPE", "Dim Type"),
        Column("VALUE", "Value"),
        Column("LOW_VALUE", "Low"),
        Column("HIGH_VALUE", "High"),
    ],
    "RATE_TABLES": [
        Column("CALENDAR", "Calendar"),
        Column("NAME", "Name"),
        Column("DESCRIPTION", "Description"),
        Column("EFFECTIVE_START_DATE", "Start Date"),
        Column("EFFECTIVE_END_DATE", "End Date"),
        Column("RATE_EXP_UNIT_TYPE", "RATE_EXP_UNIT_TYPE"),
        Column("RETURN_TYPE", "RETURN_TYPE"),
        Column("SELECTOR_UNIT_TYPE", "SELECTOR_UNIT_TYPE"),
        Column("START_VALUE_INCLUSIVE", "Start Include"),
        Column("START_VALUE", "Start"),
        Column("START_VALUE_UNIT_TYPE", "Start Type"),
        Column("END_VALUE_INCLUSIVE", "End Include"),
        Column("END_VALUE", "End"),
        Column("END_VALUE_UNIT_TYPE", "End Type"),
        Column("VALUE", "Value"),
        Column("VALUE_UNIT_TYPE", "Unit Type"),
    ],
    "QUOTA_TABLES": [
        Column("CALENDAR", "Calendar"),
        Column("NAME", "Name"),
        Column("DESCRIPTION", "Description"),
        Column("EFFECTIVE_START_DATE", "Start Date"),
        Column("EFFECTIVE_END_DATE", "End Date"),
        Column("QUOTA_PERIOD_TYPE", "Period Types"),
        Column("POSITION", "Position"),
        Column("POSITION_EFFECTIVE_START_DATE", "Position Start Date"),
        Column("POSITION_EFFECTIVE_END_DATE", "Position End Date"),
        Column("START_PERIOD", "Start Period"),
        Column("END_PERIOD", "End Period"),
        Column("UNIT_TYPE", "Value Type"),
        Column("DECIMAL_VALUE", "Value"),
    ],
    "FIXED_VALUES": [
        Column("CALENDAR", "Calendar"),
        Column("NAME", "Name"),
        Column("DESCRIPTION", "Description"),
        Column("EFFECTIVE_START_DATE", "Start Date"),
        Column("EFFECTIVE_END_DATE", "End Date"),
        Column("DECIMAL_VALUE", "Value"),
        Column("UNIT_TYPE", "Unit Type"),
    ],
    "VARIABLES": [
        Column("CALENDAR", "Calendar"),
        Column("NAME", "Name"),
        Column("DESCRIPTION", "Description"),
        Column("EFFECTIVE_START_DATE", "Start Date"),
        Column("EFFECTIVE_END_DATE", "End Date"),
        Column("RETURN_TYPE", "Return Type"),
        Column("VARIABLE_TYPE", "Variable Type"),
        Column("DEFAULT_ELEMENT_NAME", "Default"),
    ],
    "FORMULAS": [
        Column("CALENDAR", "Calendar"),
        Column("NAME", "Name"),
        Column("DESCRIPTION", "Description"),
        Column("EFFECTIVE_START_DATE", "Start Date"),
        Column("EFFECTIVE_END_DATE", "End Date"),
        Column("EXPRESSION", "Formula"),
        Column("RETURN_TYPE", "Return Type"),
    ],
    "LOG": [
        Column("Timestamp", "Timestamp"),
        Column("Module", "Module"),
        Column("Procedure", "Procedure"),
        Column("Error Number", "Error Number"),
        Column("Description", "Description"),
        Column("Context", "Context"),
    ],
}


def _row_for_sheet(row: dict[str, Any], columns: list[Column]) -> list[Any]:
    return [row.get(column.key, "") for column in columns]


def write_csv_outputs(rows: dict[str, list[dict[str, Any]]], output_dir: str | Path) -> Path:
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)

    for sheet_name, columns in SHEET_COLUMNS.items():
        csv_path = path / f"{sheet_name}.csv"
        with csv_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow([column.header for column in columns])
            for row in rows.get(sheet_name, []):
                writer.writerow(_row_for_sheet(row, columns))

    return path


def write_xlsx_output(rows: dict[str, list[dict[str, Any]]], output_path: str | Path) -> Path:
    try:
        from openpyxl import Workbook
    except ImportError as exc:  # pragma: no cover - runtime dependency branch
        raise RuntimeError(
            "openpyxl is required for XLSX output. Install with: pip install openpyxl"
        ) from exc

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    workbook = Workbook()
    default_sheet = workbook.active
    workbook.remove(default_sheet)

    for sheet_name, columns in SHEET_COLUMNS.items():
        ws = workbook.create_sheet(title=sheet_name)
        ws.append([column.header for column in columns])
        for row in rows.get(sheet_name, []):
            ws.append(_row_for_sheet(row, columns))
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = ws.dimensions

    workbook.save(path)
    return path
