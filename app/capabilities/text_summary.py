import re
from typing import Any

from app.capabilities.base import BaseCapability
from app.core.errors import BusinessValidationError


DEFAULT_MAX_LENGTH = 120


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


class TextSummaryCapability(BaseCapability):
    name = "text_summary"

    def run(self, payload: dict[str, Any]) -> str:
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

        normalized_text = normalize_text(text)
        if not normalized_text:
            raise BusinessValidationError(
                message="input.text must not be empty",
                details={"field": "text"},
            )

        max_length = payload.get("max_length", DEFAULT_MAX_LENGTH)
        if not isinstance(max_length, int) or isinstance(max_length, bool):
            raise BusinessValidationError(
                message="input.max_length must be a positive integer",
                details={"field": "max_length"},
            )

        if max_length <= 0:
            raise BusinessValidationError(
                message="input.max_length must be greater than 0",
                details={"field": "max_length"},
            )

        if len(normalized_text) <= max_length:
            return normalized_text

        return normalized_text[:max_length] + "..."
