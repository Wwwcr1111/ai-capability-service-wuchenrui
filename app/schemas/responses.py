from typing import Any

from pydantic import BaseModel


class MetaInfo(BaseModel):
    request_id: str
    capability: str | None = None
    elapsed_ms: int


class SuccessData(BaseModel):
    result: Any


class ErrorInfo(BaseModel):
    code: str
    message: str
    details: dict[str, Any]


class SuccessResponse(BaseModel):
    ok: bool
    data: SuccessData
    meta: MetaInfo


class ErrorResponse(BaseModel):
    ok: bool
    error: ErrorInfo
    meta: MetaInfo
