import time
from uuid import uuid4

from fastapi import APIRouter, Request

from app.core.logging import get_logger
from app.schemas.capability import CapabilityRunRequest, HealthResponse
from app.schemas.responses import MetaInfo, SuccessResponse
from app.services.dispatcher import dispatcher


router = APIRouter()
logger = get_logger(__name__)


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return HealthResponse(ok=True)


@router.post("/v1/capabilities/run", response_model=SuccessResponse)
async def run_capability(
    payload: CapabilityRunRequest,
    request: Request,
) -> SuccessResponse:
    start_time = time.perf_counter()
    request_id = payload.request_id or str(uuid4())

    request.state.request_id = request_id
    request.state.capability = payload.capability
    request.state.start_time = start_time

    logger.info(
        "Processing capability request capability=%s request_id=%s",
        payload.capability,
        request_id,
    )

    result = dispatcher.run(payload.capability, payload.input)
    elapsed_ms = int((time.perf_counter() - start_time) * 1000)

    return SuccessResponse(
        ok=True,
        data={"result": result},
        meta=MetaInfo(
            request_id=request_id,
            capability=payload.capability,
            elapsed_ms=elapsed_ms,
        ),
    )
