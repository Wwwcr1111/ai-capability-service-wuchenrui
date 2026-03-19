from dataclasses import dataclass, field


@dataclass
class ServiceError(Exception):
    code: str
    message: str
    status_code: int
    details: dict = field(default_factory=dict)


class CapabilityNotFoundError(ServiceError):
    def __init__(self, capability: str):
        super().__init__(
            code="CAPABILITY_NOT_FOUND",
            message=f"Unsupported capability: {capability}",
            status_code=404,
            details={"capability": capability},
        )


class BusinessValidationError(ServiceError):
    def __init__(self, message: str, details: dict | None = None):
        super().__init__(
            code="VALIDATION_ERROR",
            message=message,
            status_code=400,
            details=details or {},
        )


class RequestSchemaError(ServiceError):
    def __init__(self, message: str, details: dict | None = None):
        super().__init__(
            code="REQUEST_SCHEMA_VALIDATION_ERROR",
            message=message,
            status_code=422,
            details=details or {},
        )


class InternalServiceError(ServiceError):
    def __init__(self):
        super().__init__(
            code="INTERNAL_SERVER_ERROR",
            message="An unexpected internal error occurred",
            status_code=500,
            details={},
        )
