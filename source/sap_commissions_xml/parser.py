from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element

from .function_parser import ExpressionParser
from .logger import ParseLogger


DATA_SHEETS = [
    "PLANS",
    "COMPONENTS",
    "CREDITRULES",
    "MEASUREMENTS",
    "INCENTIVES",
    "DEPOSITS",
    "LOOKUP_TABLES",
    "RATE_TABLES",
    "QUOTA_TABLES",
    "FIXED_VALUES",
    "VARIABLES",
    "FORMULAS",
]


@dataclass(slots=True)
class ParseResult:
    rows: dict[str, list[dict[str, Any]]]
    logger: ParseLogger


class SAPCommissionsXMLParser:
    """Replicates the SAP-Commissions-XML VBA parsing workflow."""

    def __init__(self, logger: ParseLogger | None = None) -> None:
        self.logger = logger or ParseLogger()
        self.function_parser = ExpressionParser(self.logger)

    def parse_file(self, xml_path: str | Path) -> ParseResult:
        path = Path(xml_path)
        if not path.exists():
            raise FileNotFoundError(f"XML file not found: {path}")

        try:
            root = ET.parse(path).getroot()
        except ET.ParseError as exc:
            self.logger.error("mdInit", "Parse", exc, context=f"File: {path}")
            raise

        return self.parse_root(root)

    def parse_string(self, xml_content: str) -> ParseResult:
        root = ET.fromstring(xml_content)
        return self.parse_root(root)

    def parse_root(self, root: Element) -> ParseResult:
        self.logger.entries.clear()
        rows: dict[str, list[dict[str, Any]]] = {sheet: [] for sheet in DATA_SHEETS}

        for node in list(root):
            try:
                self._parse_node(node, rows)
            except Exception as exc:
                self.logger.error("mdInit", "Parse_Node", exc, context=f"Node: {_tag(node)}")

        rows["LOG"] = self.logger.as_rows()
        return ParseResult(rows=rows, logger=self.logger)

    def _parse_node(self, node: Element, rows: dict[str, list[dict[str, Any]]]) -> None:
        node_name = _tag(node)

        if node_name == "PLAN_SET":
            self._parse_plans(node, rows)
        elif node_name == "PLANCOMPONENT_SET":
            self._parse_components(node, rows)
        elif node_name == "RULE_SET":
            self._parse_rule_set(node, rows)
        elif node_name == "MD_LOOKUP_TABLE_SET":
            self._parse_lookup_tables(node, rows)
        elif node_name == "RATETABLE_SET":
            self._parse_rate_tables(node, rows)
        elif node_name == "QUOTA_SET":
            self._parse_quota_tables(node, rows)
        elif node_name == "FIXED_VALUE_SET":
            self._parse_fixed_values(node, rows)
        elif node_name == "VARIABLE_SET":
            self._parse_variables(node, rows)
        elif node_name == "FORMULA_SET":
            self._parse_formulas(node, rows)
        else:
            self.logger.warning("mdInit", "Parse_Node", f"Unsupported SET type: {node_name}")

    def _parse_rule_set(self, node: Element, rows: dict[str, list[dict[str, Any]]]) -> None:
        for rule_node in list(node):
            rule_type = rule_node.attrib.get("TYPE", "")
            rule_name = rule_node.attrib.get("NAME", "")

            if not rule_type:
                self.logger.warning(
                    "mdInit",
                    "Parse_Node",
                    "RULE node missing TYPE attribute",
                    context=f"Rule: {rule_name}",
                )
                continue

            if rule_type in {"DIRECT_TRANSACTION_CREDIT", "ROLLUP_TRANSACTION_CREDIT"}:
                self._parse_credit_rule(rule_node, rows)
            elif rule_type in {"PRIMARY_MEASUREMENT", "SECONDARY_MEASUREMENT"}:
                self._parse_measurement_rule(rule_node, rows)
            elif rule_type in {"BULK_COMMISSION", "COMMISSION"}:
                self._parse_incentive_rule(rule_node, rows)
            elif rule_type == "DEPOSIT":
                self._parse_deposit_rule(rule_node, rows)
            else:
                self.logger.warning(
                    "mdInit",
                    "Parse_Node",
                    f"Unsupported RULE TYPE: {rule_type}",
                    context=f"Rule: {rule_name}",
                )

    def _parse_plans(self, node: Element, rows: dict[str, list[dict[str, Any]]]) -> None:
        for plan_node in list(node):
            plan = dict(plan_node.attrib)
            components: list[dict[str, str]] = []

            for child in list(plan_node):
                child_name = _tag(child)
                if child_name == "COMPONENT_REF":
                    components.append(dict(child.attrib))
                elif child_name == "VARIABLE_ASSIGNMENT":
                    continue
                else:
                    self.logger.warning(
                        "PLANS",
                        "PLAN",
                        f"Unsupported child node: {child_name}",
                        context=f"Plan: {plan.get('NAME', '')}",
                    )

            for component in components:
                rows["PLANS"].append(
                    {
                        "CALENDAR": plan.get("CALENDAR", ""),
                        "NAME": plan.get("NAME", ""),
                        "DESCRIPTION": plan.get("DESCRIPTION", ""),
                        "EFFECTIVE_START_DATE": plan.get("EFFECTIVE_START_DATE", ""),
                        "EFFECTIVE_END_DATE": plan.get("EFFECTIVE_END_DATE", ""),
                        "COMPONENT_NAME": component.get("NAME", ""),
                        "COMPONENT_EFFECTIVE_START_DATE": component.get("EFFECTIVE_START_DATE", ""),
                        "COMPONENT_EFFECTIVE_END_DATE": component.get("EFFECTIVE_END_DATE", ""),
                    }
                )

    def _parse_components(self, node: Element, rows: dict[str, list[dict[str, Any]]]) -> None:
        for comp_node in list(node):
            component = dict(comp_node.attrib)
            rules: list[dict[str, str]] = []

            for child in list(comp_node):
                child_name = _tag(child)
                if child_name == "RULE_REF":
                    rules.append(dict(child.attrib))
                else:
                    self.logger.warning(
                        "COMPONENTS",
                        "COMP",
                        f"Unsupported child node: {child_name}",
                        context=f"Component: {component.get('NAME', '')}",
                    )

            for rule in rules:
                rows["COMPONENTS"].append(
                    {
                        "CALENDAR": component.get("CALENDAR", ""),
                        "NAME": component.get("NAME", ""),
                        "DESCRIPTION": component.get("DESCRIPTION", ""),
                        "EFFECTIVE_START_DATE": component.get("EFFECTIVE_START_DATE", ""),
                        "EFFECTIVE_END_DATE": component.get("EFFECTIVE_END_DATE", ""),
                        "RULE_NAME": rule.get("NAME", ""),
                        "RULE_TYPE": rule.get("TYPE", ""),
                        "RULE_EFFECTIVE_START_DATE": rule.get("EFFECTIVE_START_DATE", ""),
                        "RULE_EFFECTIVE_END_DATE": rule.get("EFFECTIVE_END_DATE", ""),
                    }
                )

    def _parse_credit_rule(self, node: Element, rows: dict[str, list[dict[str, Any]]]) -> None:
        rule = dict(node.attrib)
        rule.setdefault("RELATION_TYPE", "")
        outputs: list[dict[str, str]] = []

        for child in list(node):
            child_name = _tag(child)
            if child_name == "ACTION_EXPRESSION_SET":
                outputs = self._parse_credit_action_set(child, rule.get("TYPE", ""))
            elif child_name == "CONDITION_EXPRESSION":
                rule["CONDITION"] = self.function_parser.parse(_first_child(child))
            elif child_name == "EVENT_TYPE_EXPRESSION":
                rule["EVENT_TYPE"] = self.function_parser.parse(_first_child(child))
            elif child_name == "ROLLUP_EXPRESSION_SET":
                rollup_relation = self._find_descendant_text(
                    child,
                    ["ROLLUP_EXPRESSION", "RELATION_TYPE"],
                )
                if rollup_relation:
                    rule["RELATION_TYPE"] = rollup_relation
            else:
                self.logger.warning(
                    "CREDITRULES",
                    "RULE",
                    f"Unsupported child node: {child_name}",
                    context=f"Rule: {rule.get('NAME', '')}",
                )

        for output in outputs:
            row = {
                "CALENDAR": rule.get("CALENDAR", ""),
                "NAME": rule.get("NAME", ""),
                "DESCRIPTION": rule.get("DESCRIPTION", ""),
                "EFFECTIVE_START_DATE": rule.get("EFFECTIVE_START_DATE", ""),
                "EFFECTIVE_END_DATE": rule.get("EFFECTIVE_END_DATE", ""),
                "CONDITION": rule.get("CONDITION", ""),
                "EVENT_TYPE": rule.get("EVENT_TYPE", ""),
                "RULE_TYPE": rule.get("TYPE", ""),
                "RELATION_TYPE": rule.get("RELATION_TYPE", ""),
                "OUTPUT_NAME": output.get("NAME", ""),
                "DISPLAY_NAME_FOR_REPORTS": output.get("DISPLAY_NAME_FOR_REPORTS", ""),
                "IS_REPORTABLE": output.get("IS_REPORTABLE", ""),
                "PERIOD_TYPE": output.get("PERIOD_TYPE", ""),
                "OUTPUT_TYPE": output.get("TYPE", ""),
                "UNIT_TYPE": output.get("UNIT_TYPE", ""),
                "VALUE": output.get("VALUE", ""),
                "HOLD_REF_NAME": output.get("HOLD_REF_NAME", ""),
                "HOLD_REF_PERIOD_TYPE": output.get("HOLD_REF_PERIOD_TYPE", ""),
                "OUTPUT_CONDITION": output.get("CONDITION", ""),
                "CREDIT_TYPE": output.get("CREDIT_TYPE", ""),
                "DUPLICATE": output.get("DUPLICATE", ""),
                "ROLL_UP": output.get("ROLL_UP", ""),
                "ROLL_DATE": output.get("ROLL_DATE", ""),
            }
            row.update(self._metric_columns(output))
            rows["CREDITRULES"].append(row)

    def _parse_credit_action_set(self, node: Element, rule_type: str) -> list[dict[str, str]]:
        output: list[dict[str, str]] = []

        for action_expression in list(node):
            first = _first_child(action_expression)
            if first is None:
                continue
            if _tag(first) != "FUNCTION":
                self.logger.warning(
                    "CREDITRULES",
                    "ACTION_SET",
                    f"Unexpected ACTION_EXPRESSION child: {_tag(first)}",
                )
                continue
            output.append(self._parse_credit_action_function(first, rule_type))

        return output

    def _parse_credit_action_function(self, node: Element, rule_type: str) -> dict[str, str]:
        function_id = node.attrib.get("ID", "")

        if rule_type == "DIRECT_TRANSACTION_CREDIT":
            if function_id != "DIRECT_TRANSACTION_CREDIT_ALLGAs":
                self.logger.warning(
                    "CREDITRULES",
                    "ACTION_FUNCTION",
                    f"Unexpected FUNCTION ID for DIRECT_TRANSACTION_CREDIT: {function_id}",
                )
            return self._parse_credit_action_body(node, procedure="ACTION_DIRECT")

        if rule_type == "ROLLUP_TRANSACTION_CREDIT":
            if function_id != "INDIRECT_TRANSACTION_CREDIT_ALLGAs":
                self.logger.warning(
                    "CREDITRULES",
                    "ACTION_FUNCTION",
                    f"Unexpected FUNCTION ID for ROLLUP_TRANSACTION_CREDIT: {function_id}",
                )
            return self._parse_credit_action_body(node, procedure="ACTION_ROLLUP")

        self.logger.warning(
            "CREDITRULES",
            "ACTION_FUNCTION",
            f"Unsupported credit rule type: {rule_type}",
        )
        return {}

    def _parse_credit_action_body(self, node: Element, procedure: str) -> dict[str, str]:
        action: dict[str, str] = {}
        children = list(node)

        try:
            output_ref = self._child(children, 0)
            if output_ref is not None:
                action.update(output_ref.attrib)

            action["VALUE"] = self.function_parser.parse(self._child(children, 1))

            hold_ref = self._child(children, 2)
            if hold_ref is not None:
                for key, value in hold_ref.attrib.items():
                    action[f"HOLD_REF_{key}"] = value

            action["CONDITION"] = self.function_parser.parse(self._child(children, 3))
            action["CREDIT_TYPE"] = _node_text(self._child(children, 4))
            action["DUPLICATE"] = self.function_parser.parse(self._child(children, 5))
            action["ROLL_UP"] = self.function_parser.parse(self._child(children, 6))
            action["ROLL_DATE"] = self.function_parser.parse(self._child(children, 7))

            for i in range(1, 17):
                action[f"GA{i}"] = self.function_parser.parse(self._child(children, i + 7))
            for i in range(1, 7):
                action[f"GN{i}"] = self.function_parser.parse(self._child(children, i + 23))
            for i in range(1, 7):
                action[f"GD{i}"] = self.function_parser.parse(self._child(children, i + 29))
            for i in range(1, 7):
                action[f"GB{i}"] = self.function_parser.parse(self._child(children, i + 35))

        except Exception as exc:
            self.logger.error("CREDITRULES", procedure, exc)

        return action

    def _parse_measurement_rule(self, node: Element, rows: dict[str, list[dict[str, Any]]]) -> None:
        rule = dict(node.attrib)
        outputs: list[dict[str, str]] = []

        for child in list(node):
            child_name = _tag(child)
            if child_name == "ACTION_EXPRESSION_SET":
                outputs = self._parse_measurement_action_set(child)
            elif child_name == "CONDITION_EXPRESSION":
                rule["CONDITION"] = self.function_parser.parse(_first_child(child))
            else:
                self.logger.warning(
                    "MEASUREMENTS",
                    "RULE",
                    f"Unsupported child node: {child_name}",
                    context=f"Rule: {rule.get('NAME', '')}",
                )

        for output in outputs:
            row = {
                "CALENDAR": rule.get("CALENDAR", ""),
                "NAME": rule.get("NAME", ""),
                "DESCRIPTION": rule.get("DESCRIPTION", ""),
                "EFFECTIVE_START_DATE": rule.get("EFFECTIVE_START_DATE", ""),
                "EFFECTIVE_END_DATE": rule.get("EFFECTIVE_END_DATE", ""),
                "CONDITION": rule.get("CONDITION", ""),
                "RULE_TYPE": rule.get("TYPE", ""),
                "OUTPUT_NAME": output.get("NAME", ""),
                "DISPLAY_NAME_FOR_REPORTS": output.get("DISPLAY_NAME_FOR_REPORTS", ""),
                "IS_REPORTABLE": output.get("IS_REPORTABLE", ""),
                "PERIOD_TYPE": output.get("PERIOD_TYPE", ""),
                "OUTPUT_TYPE": output.get("TYPE", ""),
                "UNIT_TYPE": output.get("UNIT_TYPE", ""),
                "VALUE": output.get("VALUE", ""),
            }
            row.update(self._metric_columns(output))
            rows["MEASUREMENTS"].append(row)

    def _parse_measurement_action_set(self, node: Element) -> list[dict[str, str]]:
        actions: list[dict[str, str]] = []
        for action_expression in list(node):
            action_node = _first_child(action_expression)
            if action_node is None:
                continue
            actions.append(self._parse_measurement_action(action_node))
        return actions

    def _parse_measurement_action(self, node: Element) -> dict[str, str]:
        action: dict[str, str] = {}
        children = list(node)

        output_ref = self._child(children, 0)
        if output_ref is not None:
            action.update(output_ref.attrib)

        action["VALUE"] = self.function_parser.parse(self._child(children, 1))

        if node.attrib.get("RULE_TYPES") == "SECONDARY_MEASUREMENT":
            for i in range(1, 17):
                action[f"GA{i}"] = self.function_parser.parse(self._child(children, i + 1))
            for i in range(1, 7):
                action[f"GN{i}"] = self.function_parser.parse(self._child(children, i + 17))
            for i in range(1, 7):
                action[f"GD{i}"] = self.function_parser.parse(self._child(children, i + 23))
            for i in range(1, 7):
                action[f"GB{i}"] = self.function_parser.parse(self._child(children, i + 29))

        return action

    def _parse_incentive_rule(self, node: Element, rows: dict[str, list[dict[str, Any]]]) -> None:
        rule = dict(node.attrib)
        outputs: list[dict[str, str]] = []

        for child in list(node):
            child_name = _tag(child)
            if child_name == "ACTION_EXPRESSION_SET":
                outputs = self._parse_incentive_action_set(child)
            elif child_name == "CONDITION_EXPRESSION":
                rule["CONDITION"] = self.function_parser.parse(_first_child(child))
            elif child_name == "INPUT_EXPRESSION_SET":
                # COMMISSION rules commonly store their input expression here
                # instead of CONDITION_EXPRESSION.
                first_input = _first_child(child)
                if first_input is not None:
                    rule["CONDITION"] = self.function_parser.parse(_first_child(first_input))
            else:
                self.logger.warning(
                    "INCENTIVES",
                    "RULE",
                    f"Unsupported child node: {child_name}",
                    context=f"Rule: {rule.get('NAME', '')}",
                )

        for output in outputs:
            row = {
                "CALENDAR": rule.get("CALENDAR", ""),
                "NAME": rule.get("NAME", ""),
                "DESCRIPTION": rule.get("DESCRIPTION", ""),
                "EFFECTIVE_START_DATE": rule.get("EFFECTIVE_START_DATE", ""),
                "EFFECTIVE_END_DATE": rule.get("EFFECTIVE_END_DATE", ""),
                "CONDITION": rule.get("CONDITION", ""),
                "RULE_TYPE": rule.get("TYPE", ""),
                "OUTPUT_NAME": output.get("NAME", ""),
                "DISPLAY_NAME_FOR_REPORTS": output.get("DISPLAY_NAME_FOR_REPORTS", ""),
                "IS_REPORTABLE": output.get("IS_REPORTABLE", ""),
                "PERIOD_TYPE": output.get("PERIOD_TYPE", ""),
                "OUTPUT_TYPE": output.get("TYPE", ""),
                "UNIT_TYPE": output.get("UNIT_TYPE", ""),
                "VALUE": output.get("VALUE", ""),
                "RATE": output.get("RATE", ""),
                "HOLD_REF_NAME": output.get("HOLD_REF_NAME", ""),
                "HOLD_REF_PERIOD_OFFSET": output.get("HOLD_REF_PERIOD_OFFSET", ""),
                "HOLD_REF_PERIOD_TYPE": output.get("HOLD_REF_PERIOD_TYPE", ""),
            }
            row.update(self._metric_columns(output))
            rows["INCENTIVES"].append(row)

    def _parse_incentive_action_set(self, node: Element) -> list[dict[str, str]]:
        actions: list[dict[str, str]] = []
        for action_expression in list(node):
            action_node = _first_child(action_expression)
            if action_node is None:
                continue
            actions.append(self._parse_incentive_action(action_node))
        return actions

    def _parse_incentive_action(self, node: Element) -> dict[str, str]:
        action: dict[str, str] = {}
        children = list(node)

        output_ref = self._child(children, 0)
        if output_ref is not None:
            action.update(output_ref.attrib)

        action["VALUE"] = self.function_parser.parse(self._child(children, 1))

        hold_ref = self._child(children, 2)
        if hold_ref is not None:
            for key, value in hold_ref.attrib.items():
                action[f"HOLD_REF_{key}"] = value

        action["RATE"] = self.function_parser.parse(self._child(children, 3))

        if node.attrib.get("RULE_TYPES") in {"BULK_COMMISSION", "COMMISSION"}:
            if len(children) < 35:
                self.logger.warning(
                    "INCENTIVES",
                    "ACTION",
                    "Commission action has fewer than 35 child nodes; skipping GA/GN/GD/GB parsing",
                    context=f"Action ID: {node.attrib.get('ID', '')}",
                )
                return action
            x = len(children) - 35
            for i in range(1, 17):
                action[f"GA{i}"] = self.function_parser.parse(self._child(children, i + x))
            x += 16
            for i in range(1, 7):
                action[f"GN{i}"] = self.function_parser.parse(self._child(children, i + x))
            x += 6
            for i in range(1, 7):
                action[f"GD{i}"] = self.function_parser.parse(self._child(children, i + x))
            x += 6
            for i in range(1, 7):
                action[f"GB{i}"] = self.function_parser.parse(self._child(children, i + x))

        return action

    def _parse_deposit_rule(self, node: Element, rows: dict[str, list[dict[str, Any]]]) -> None:
        rule = dict(node.attrib)
        outputs: list[dict[str, str]] = []

        for child in list(node):
            child_name = _tag(child)
            if child_name == "ACTION_EXPRESSION_SET":
                outputs = self._parse_deposit_action_set(child)
            elif child_name == "CONDITION_EXPRESSION":
                rule["CONDITION"] = self.function_parser.parse(_first_child(child))
            else:
                self.logger.warning(
                    "DEPOSITS",
                    "RULE",
                    f"Unsupported child node: {child_name}",
                    context=f"Rule: {rule.get('NAME', '')}",
                )

        for output in outputs:
            row = {
                "CALENDAR": rule.get("CALENDAR", ""),
                "NAME": rule.get("NAME", ""),
                "DESCRIPTION": rule.get("DESCRIPTION", ""),
                "EFFECTIVE_START_DATE": rule.get("EFFECTIVE_START_DATE", ""),
                "EFFECTIVE_END_DATE": rule.get("EFFECTIVE_END_DATE", ""),
                "CONDITION": rule.get("CONDITION", ""),
                "RULE_TYPE": rule.get("TYPE", ""),
                "OUTPUT_NAME": output.get("NAME", ""),
                "DISPLAY_NAME_FOR_REPORTS": output.get("DISPLAY_NAME_FOR_REPORTS", ""),
                "IS_REPORTABLE": output.get("IS_REPORTABLE", ""),
                "PERIOD_TYPE": output.get("PERIOD_TYPE", ""),
                "OUTPUT_TYPE": output.get("TYPE", ""),
                "UNIT_TYPE": output.get("UNIT_TYPE", ""),
                "VALUE": output.get("VALUE", ""),
                "HOLD_REF_NAME": output.get("HOLD_REF_NAME", ""),
                "HOLD_CONDITION": output.get("HOLD_CONDITION", ""),
                "EARNING_GROUP": output.get("EARNING_GROUP", ""),
                "EARNING_CODE": output.get("EARNING_CODE", ""),
            }
            row.update(self._metric_columns(output))
            rows["DEPOSITS"].append(row)

    def _parse_deposit_action_set(self, node: Element) -> list[dict[str, str]]:
        actions: list[dict[str, str]] = []
        for action_expression in list(node):
            action_node = _first_child(action_expression)
            if action_node is None:
                continue
            actions.append(self._parse_deposit_action(action_node))
        return actions

    def _parse_deposit_action(self, node: Element) -> dict[str, str]:
        action: dict[str, str] = {}
        children = list(node)

        output_ref = self._child(children, 0)
        if output_ref is not None:
            action.update(output_ref.attrib)

        action["EARNING_CODE"] = self.function_parser.parse(self._child(children, 1))
        action["EARNING_GROUP"] = self.function_parser.parse(self._child(children, 2))
        action["VALUE"] = self.function_parser.parse(self._child(children, 3))

        hold_ref = self._child(children, 4)
        if hold_ref is not None:
            for key, value in hold_ref.attrib.items():
                action[f"HOLD_REF_{key}"] = value
            action["HOLD_CONDITION"] = _node_text(hold_ref)

        for i in range(1, 17):
            action[f"GA{i}"] = self.function_parser.parse(self._child(children, i + 4))
        for i in range(1, 7):
            action[f"GN{i}"] = self.function_parser.parse(self._child(children, i + 20))
        for i in range(1, 7):
            action[f"GD{i}"] = self.function_parser.parse(self._child(children, i + 26))
        for i in range(1, 7):
            action[f"GB{i}"] = self.function_parser.parse(self._child(children, i + 32))

        return action

    def _parse_lookup_tables(self, node: Element, rows: dict[str, list[dict[str, Any]]]) -> None:
        for table_node in list(node):
            table = dict(table_node.attrib)

            first_child = self._child(list(table_node), 0)
            if first_child is None:
                continue
            table.update(first_child.attrib)

            dimensions: list[dict[str, str]] = []
            for dim_group in list(first_child):
                if _tag(dim_group) != "DIM_NAME":
                    continue
                for dim_cell in list(dim_group):
                    dimension = dict(dim_group.attrib)
                    dimension.update(dim_cell.attrib)
                    dimensions.append(dimension)

            for dimension in dimensions:
                rows["LOOKUP_TABLES"].append(
                    {
                        "CALENDAR": table.get("CALENDAR", ""),
                        "NAME": table.get("NAME", ""),
                        "DESCRIPTION": table.get("DESCRIPTION", ""),
                        "EFFECTIVE_START_DATE": table.get("EFFECTIVE_START_DATE", ""),
                        "EFFECTIVE_END_DATE": table.get("EFFECTIVE_END_DATE", ""),
                        "UNIT_TYPE": table.get("UNIT_TYPE", ""),
                        "CONVERT_NULL_VALUE": table.get("CONVERT_NULL_VALUE", ""),
                        "DIM_NAME": dimension.get("DIM_NAME", ""),
                        "DIM_EFFECTIVE_START_DATE": dimension.get("EFFECTIVE_START_DATE", ""),
                        "DIM_EFFECTIVE_END_DATE": dimension.get("EFFECTIVE_END_DATE", ""),
                        "CASE_SENSITIVE": dimension.get("CASE_SENSITIVE", ""),
                        "DIM_TYPE": dimension.get("TYPE", ""),
                        "VALUE": dimension.get("VALUE", ""),
                        "LOW_VALUE": dimension.get("LOW_VALUE", ""),
                        "HIGH_VALUE": dimension.get("HIGH_VALUE", ""),
                    }
                )

    def _parse_rate_tables(self, node: Element, rows: dict[str, list[dict[str, Any]]]) -> None:
        for rate_table_node in list(node):
            table = dict(rate_table_node.attrib)
            selectors: list[dict[str, str]] = []

            for selector_group in list(rate_table_node):
                selector: dict[str, str] = {}
                for selector_node in list(selector_group):
                    selector_name = _tag(selector_node)
                    values = list(selector_node.attrib.values())

                    if selector_name in {"START_VALUE", "END_VALUE"}:
                        selector[selector_name] = values[0] if len(values) > 0 else ""
                        selector[f"{selector_name}_INCLUSIVE"] = values[1] if len(values) > 1 else ""
                        selector[f"{selector_name}_UNIT_TYPE"] = values[2] if len(values) > 2 else ""
                    else:
                        selector[selector_name] = values[0] if len(values) > 0 else ""
                        selector[f"{selector_name}_UNIT_TYPE"] = values[1] if len(values) > 1 else ""

                selectors.append(selector)

            for selector in selectors:
                rows["RATE_TABLES"].append(
                    {
                        "CALENDAR": table.get("CALENDAR", ""),
                        "NAME": table.get("NAME", ""),
                        "DESCRIPTION": table.get("DESCRIPTION", ""),
                        "EFFECTIVE_START_DATE": table.get("EFFECTIVE_START_DATE", ""),
                        "EFFECTIVE_END_DATE": table.get("EFFECTIVE_END_DATE", ""),
                        "RATE_EXP_UNIT_TYPE": table.get("RATE_EXP_UNIT_TYPE", ""),
                        "RETURN_TYPE": table.get("RETURN_TYPE", ""),
                        "SELECTOR_UNIT_TYPE": table.get("SELECTOR_UNIT_TYPE", ""),
                        "START_VALUE_INCLUSIVE": selector.get("START_VALUE_INCLUSIVE", ""),
                        "START_VALUE": selector.get("START_VALUE", ""),
                        "START_VALUE_UNIT_TYPE": selector.get("START_VALUE_UNIT_TYPE", ""),
                        "END_VALUE_INCLUSIVE": selector.get("END_VALUE_INCLUSIVE", ""),
                        "END_VALUE": selector.get("END_VALUE", ""),
                        "END_VALUE_UNIT_TYPE": selector.get("END_VALUE_UNIT_TYPE", ""),
                        "VALUE": selector.get("VALUE", ""),
                        "VALUE_UNIT_TYPE": selector.get("VALUE_UNIT_TYPE", ""),
                    }
                )

    def _parse_quota_tables(self, node: Element, rows: dict[str, list[dict[str, Any]]]) -> None:
        for quota_table_node in list(node):
            table = dict(quota_table_node.attrib)

            quota_period_types: list[str] = []
            for child in list(quota_table_node):
                if _tag(child) == "QUOTA_PERIOD_TYPE":
                    quota_period_types.extend(child.attrib.values())
                else:
                    break
            table["QUOTA_PERIOD_TYPE"] = ", ".join(quota_period_types)

            quota_position: dict[str, str] = {}
            quotas: list[dict[str, str]] = []

            for child in list(quota_table_node):
                if _tag(child) != "QUOTA_VALUE_SET":
                    continue

                for quota_value_node in list(child):
                    quota_tag = _tag(quota_value_node)
                    if quota_tag == "QUOTA_POSITION":
                        quota_position = dict(quota_value_node.attrib)
                    elif quota_tag == "QUOTA_VALUE":
                        quota = dict(quota_position)
                        quota.update(quota_value_node.attrib)
                        quotas.append(quota)

            for quota in quotas:
                rows["QUOTA_TABLES"].append(
                    {
                        "CALENDAR": table.get("CALENDAR", ""),
                        "NAME": table.get("NAME", ""),
                        "DESCRIPTION": table.get("DESCRIPTION", ""),
                        "EFFECTIVE_START_DATE": table.get("EFFECTIVE_START_DATE", ""),
                        "EFFECTIVE_END_DATE": table.get("EFFECTIVE_END_DATE", ""),
                        "QUOTA_PERIOD_TYPE": table.get("QUOTA_PERIOD_TYPE", ""),
                        "POSITION": quota.get("NAME", ""),
                        "POSITION_EFFECTIVE_START_DATE": quota.get("EFFECTIVE_START_DATE", ""),
                        "POSITION_EFFECTIVE_END_DATE": quota.get("EFFECTIVE_END_DATE", ""),
                        "START_PERIOD": quota.get("START_PERIOD", ""),
                        "END_PERIOD": quota.get("END_PERIOD", ""),
                        "UNIT_TYPE": quota.get("UNIT_TYPE", ""),
                        "DECIMAL_VALUE": quota.get("DECIMAL_VALUE", ""),
                    }
                )

    def _parse_fixed_values(self, node: Element, rows: dict[str, list[dict[str, Any]]]) -> None:
        for fixed_node in list(node):
            fixed_value = dict(fixed_node.attrib)
            rows["FIXED_VALUES"].append(
                {
                    "CALENDAR": fixed_value.get("CALENDAR", ""),
                    "NAME": fixed_value.get("NAME", ""),
                    "DESCRIPTION": fixed_value.get("DESCRIPTION", ""),
                    "EFFECTIVE_START_DATE": fixed_value.get("EFFECTIVE_START_DATE", ""),
                    "EFFECTIVE_END_DATE": fixed_value.get("EFFECTIVE_END_DATE", ""),
                    "DECIMAL_VALUE": fixed_value.get("DECIMAL_VALUE", ""),
                    "UNIT_TYPE": fixed_value.get("UNIT_TYPE", ""),
                }
            )

    def _parse_variables(self, node: Element, rows: dict[str, list[dict[str, Any]]]) -> None:
        for variable_node in list(node):
            variable = dict(variable_node.attrib)
            rows["VARIABLES"].append(
                {
                    "CALENDAR": variable.get("CALENDAR", ""),
                    "NAME": variable.get("NAME", ""),
                    "DESCRIPTION": variable.get("DESCRIPTION", ""),
                    "EFFECTIVE_START_DATE": variable.get("EFFECTIVE_START_DATE", ""),
                    "EFFECTIVE_END_DATE": variable.get("EFFECTIVE_END_DATE", ""),
                    "RETURN_TYPE": variable.get("RETURN_TYPE", ""),
                    "VARIABLE_TYPE": variable.get("VARIABLE_TYPE", ""),
                    "DEFAULT_ELEMENT_NAME": variable.get("DEFAULT_ELEMENT_NAME", ""),
                }
            )

    def _parse_formulas(self, node: Element, rows: dict[str, list[dict[str, Any]]]) -> None:
        for formula_node in list(node):
            formula = dict(formula_node.attrib)
            expression = ""

            expression_group = _first_child(formula_node)
            if expression_group is not None:
                expression = self.function_parser.parse(_first_child(expression_group))
            formula["EXPRESSION"] = expression

            rows["FORMULAS"].append(
                {
                    "CALENDAR": formula.get("CALENDAR", ""),
                    "NAME": formula.get("NAME", ""),
                    "DESCRIPTION": formula.get("DESCRIPTION", ""),
                    "EFFECTIVE_START_DATE": formula.get("EFFECTIVE_START_DATE", ""),
                    "EFFECTIVE_END_DATE": formula.get("EFFECTIVE_END_DATE", ""),
                    "EXPRESSION": formula.get("EXPRESSION", ""),
                    "RETURN_TYPE": formula.get("RETURN_TYPE", ""),
                }
            )

    def _metric_columns(self, source: dict[str, str]) -> dict[str, str]:
        output: dict[str, str] = {}
        for i in range(1, 17):
            output[f"GA{i}"] = source.get(f"GA{i}", "")
        for i in range(1, 7):
            output[f"GN{i}"] = source.get(f"GN{i}", "")
        for i in range(1, 7):
            output[f"GD{i}"] = source.get(f"GD{i}", "")
        for i in range(1, 7):
            output[f"GB{i}"] = source.get(f"GB{i}", "")
        return output

    def _find_descendant_text(self, node: Element, path: list[str]) -> str:
        current = node
        for part in path:
            children = [child for child in list(current) if _tag(child) == part]
            if not children:
                return ""
            current = children[0]
        return _node_text(current)

    @staticmethod
    def _child(children: list[Element], index: int) -> Element | None:
        if 0 <= index < len(children):
            return children[index]
        return None


def _tag(node: Element) -> str:
    if "}" in node.tag:
        return node.tag.split("}", 1)[1]
    return node.tag


def _node_text(node: Element | None) -> str:
    if node is None:
        return ""
    return (node.text or "").strip()


def _first_child(node: Element | None) -> Element | None:
    if node is None:
        return None
    children = list(node)
    return children[0] if children else None
