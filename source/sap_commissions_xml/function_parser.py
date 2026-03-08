from __future__ import annotations

from xml.etree.ElementTree import Element

from .logger import ParseLogger


_SUPPORTED_LITERAL_TAGS = {
    "UNIT_TYPE",
    "CREDIT_TYPE",
    "BOOLEAN",
    "DATA_FIELD",
    "PERIOD_TYPE",
    "RELATION_TYPE",
    "STANDARD_PERIOD",
}

_REF_TAGS = {
    "MDLTVAR_REF",
    "RULE_ELEMENT_REF",
    "MEASUREMENT_REF",
    "INCENTIVE_REF",
    "MDLT_REF",
}

_OPERATOR_MAP = {
    # Modernized IDs
    "ISEQUALTO_OPERATOR": " = ",
    "NOTEQUALTO_OPERATOR": " <> ",
    "AND_OPERATOR": " AND ",
    "OR_OPERATOR": " OR ",
    "MULTIPLY_OPERATOR": " * ",
    "DIVISION_OPERATOR": " / ",
    "ADDITION_OPERATOR": " + ",
    "SUBTRACTION_OPERATOR": " - ",
    "LESSTHAN_OPERATOR": " < ",
    "LESSTHANOREQUALTO_OPERATOR": " <= ",
    "GREATERTHAN_OPERATOR": " > ",
    "GREATERTHANOREQUALTO_OPERATOR": " >= ",
    "NOT_OPERATOR": "NOT ",
    # Legacy IDs
    "SUBTRACT_OPERATOR": " - ",
    "ADD_OPERATOR": " + ",
    "GREATERTHANEQUALTO_OPERATOR": " >= ",
    "LESSTHANEQUALTO_OPERATOR": " <= ",
    "NOT_BOOLEAN_OPERATOR": " != ",
}


class ExpressionParser:
    """Equivalent of mdFunctions.Parse_Function in the VBA project."""

    def __init__(self, logger: ParseLogger) -> None:
        self.logger = logger

    def parse(self, node: Element | None) -> str:
        if node is None:
            return ""

        tag = _tag(node)
        try:
            if tag in _SUPPORTED_LITERAL_TAGS:
                parsed = _node_text(node)
            elif tag in _REF_TAGS:
                parsed = node.attrib.get("NAME", "")
            elif tag == "FUNCTION":
                parsed = self._parse_function_call(node)
            elif tag == "OPERATOR":
                parsed = self._parse_operator(node)
            elif tag == "STRING_LITERAL":
                txt = _node_text(node)
                parsed = "-" if txt == "NULL" else f'"{txt}"'
            elif tag == "VALUE":
                parsed = next(iter(node.attrib.values()), "")
            else:
                self.logger.warning(
                    "mdFunctions",
                    "Parse_Function",
                    f"Unsupported node type: {tag}",
                )
                parsed = f"[{tag}]"

            parsed = self._append_attribute_suffixes(parsed, node)
            return parsed
        except Exception as exc:
            self.logger.error("mdFunctions", "Parse_Function", exc, context=f"Node: {tag}")
            return "[ERROR]"

    def _parse_function_call(self, node: Element) -> str:
        func_name = node.attrib.get("ID", "")
        try:
            parts = [self.parse(child) for child in list(node)]
            return f"{func_name}({', '.join(parts)})"
        except Exception as exc:
            self.logger.error("mdFunctions", "F_Parse", exc, context=f"FuncName: {func_name}")
            return f"[ERROR:{func_name}]"

    def _parse_operator(self, node: Element) -> str:
        op_id = node.attrib.get("ID", "")
        try:
            operator = _OPERATOR_MAP.get(op_id)
            if operator is None:
                self.logger.warning("mdFunctions", "O_Parse", f"Unknown operator: {op_id}")
                operator = f" [{op_id}] "

            children = list(node)
            if not children:
                return operator.strip()

            left_side = self.parse(children[0])
            if len(children) > 1:
                expression = left_side + operator + self.parse(children[1])
            else:
                expression = operator + left_side

            wrapped = len(node.attrib) == 2
            if wrapped:
                expression = f"({expression})"
            return expression
        except Exception as exc:
            self.logger.error("mdFunctions", "O_Parse", exc, context=f"Operator: {op_id}")
            return "[ERROR]"

    def _append_attribute_suffixes(self, parsed: str, node: Element) -> str:
        for attr_name, attr_value in node.attrib.items():
            if attr_name == "PERIOD_OFFSET" and attr_value != "0":
                parsed += f"-{attr_value}"
            if attr_name == "RELATION_TYPE":
                parsed += f"({attr_value})"
            if attr_name == "PERIOD_TYPE":
                parsed += f":{attr_value}"
        return parsed


def _tag(node: Element) -> str:
    if "}" in node.tag:
        return node.tag.split("}", 1)[1]
    return node.tag


def _node_text(node: Element) -> str:
    return (node.text or "").strip()
