from typing import Any

from app.capabilities.base import BaseCapability
from app.core.errors import BusinessValidationError


class TextStatsCapability(BaseCapability):
    name = "text_stats"

    def run(self, payload: dict[str, Any]) -> dict[str, int]:
        if "text" not in payload:
            raise BusinessValidationError(
                message="input.text is required",
                details={"field": "text"},
            )

        text = payload["text"]
        if not isinstance(text, str):
            raise BusinessValidationError(
                message="input.text must be a string",
                details={"field": "text"},
            )

        if not text.strip():
            raise BusinessValidationError(
                message="input.text must not be empty",
                details={"field": "text"},
            )

        return {
            "char_count": len(text),
            "word_count": len(text.split()),
            "line_count": len(text.splitlines()) or 1,
        }
