import time
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.errors import InternalServiceError, RequestSchemaError, ServiceError
from app.core.logging import get_logger


logger = get_logger(__name__)


def _build_meta(request: Request) -> dict[str, Any]:
    start_time = getattr(request.state, "start_time", None)
    elapsed_ms = int((time.perf_counter() - start_time) * 1000) if start_time else 0
    request_id = getattr(request.state, "request_id", None) or str(uuid4())
    capability = getattr(request.state, "capability", None)
    return {
        "request_id": request_id,
        "capability": capability,
        "elapsed_ms": elapsed_ms,
    }


def _error_response(request: Request, error: ServiceError) -> JSONResponse:
    meta = _build_meta(request)
    return JSONResponse(
        status_code=error.status_code,
        content={
            "ok": False,
            "error": {
                "code": error.code,
                "message": error.message,
                "details": error.details,
            },
            "meta": meta,
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ServiceError)
    async def service_error_handler(request: Request, exc: ServiceError) -> JSONResponse:
        logger.error(
            "Service error request_id=%s capability=%s code=%s message=%s",
            getattr(request.state, "request_id", None),
            getattr(request.state, "capability", None),
            exc.code,
            exc.message,
        )
        return _error_response(request, exc)

    @app.exception_handler(RequestValidationError)
    async def request_validation_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        body = exc.body if isinstance(exc.body, dict) else {}
        request.state.request_id = body.get("request_id") or getattr(
            request.state, "request_id", None
        ) or str(uuid4())
        request.state.capability = body.get("capability") or getattr(
            request.state, "capability", None
        )

        details = {"errors": exc.errors()}
        schema_error = RequestSchemaError(
            message="Request body validation failed",
            details=details,
        )
        logger.error(
            "Request validation error request_id=%s capability=%s",
            request.state.request_id,
            request.state.capability,
        )
        return _error_response(request, schema_error)

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        error = InternalServiceError()
        logger.exception(
            "Unhandled error request_id=%s capability=%s",
            getattr(request.state, "request_id", None),
            getattr(request.state, "capability", None),
        )
        return _error_response(request, error)
