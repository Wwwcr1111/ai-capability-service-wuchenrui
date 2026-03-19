from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class HealthResponse(BaseModel):
    ok: bool = True


class CapabilityRunRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    capability: str = Field(..., description="Capability name to execute")
    input: dict[str, Any] = Field(..., description="Capability input payload")
    request_id: str | None = Field(
        default=None,
        description="Optional client-provided request identifier",
    )
