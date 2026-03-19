from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router
from app.core.exception_handlers import register_exception_handlers
from app.core.logging import configure_logging, get_logger


configure_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("AI capability service started")
    yield


app = FastAPI(
    title="AI Capability Service",
    version="0.1.0",
    lifespan=lifespan,
)

register_exception_handlers(app)
app.include_router(router)
