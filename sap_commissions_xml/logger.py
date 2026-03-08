from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class LogEntry:
    """Represents a single warning/error entry."""

    timestamp: str
    module: str
    procedure: str
    error_number: str
    description: str
    context: str


class ParseLogger:
    """Collects warnings and errors in the same shape as the VBA LOG sheet."""

    def __init__(self) -> None:
        self.entries: list[LogEntry] = []

    def warning(self, module: str, procedure: str, message: str, context: str = "") -> None:
        self.entries.append(
            LogEntry(
                timestamp=self._now(),
                module=module,
                procedure=procedure,
                error_number="WARNING",
                description=message,
                context=context,
            )
        )

    def error(self, module: str, procedure: str, exc: Exception, context: str = "") -> None:
        self.entries.append(
            LogEntry(
                timestamp=self._now(),
                module=module,
                procedure=procedure,
                error_number=type(exc).__name__,
                description=str(exc),
                context=context,
            )
        )

    def as_rows(self) -> list[dict[str, Any]]:
        return [
            {
                "Timestamp": entry.timestamp,
                "Module": entry.module,
                "Procedure": entry.procedure,
                "Error Number": entry.error_number,
                "Description": entry.description,
                "Context": entry.context,
            }
            for entry in self.entries
        ]

    def count_warnings(self) -> int:
        return sum(1 for entry in self.entries if entry.error_number == "WARNING")

    def count_errors(self) -> int:
        return sum(1 for entry in self.entries if entry.error_number != "WARNING")

    @staticmethod
    def _now() -> str:
        return datetime.now().isoformat(sep=" ", timespec="seconds")
