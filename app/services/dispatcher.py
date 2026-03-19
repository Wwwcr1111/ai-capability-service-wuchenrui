from typing import Any

from app.capabilities.base import BaseCapability
from app.capabilities.text_stats import TextStatsCapability
from app.capabilities.text_summary import TextSummaryCapability
from app.core.errors import CapabilityNotFoundError


class CapabilityDispatcher:
    def __init__(self, capabilities: list[BaseCapability]):
        self._registry = {capability.name: capability for capability in capabilities}

    def run(self, capability_name: str, payload: dict[str, Any]) -> Any:
        capability = self._registry.get(capability_name)
        if capability is None:
            raise CapabilityNotFoundError(capability_name)
        return capability.run(payload)


dispatcher = CapabilityDispatcher(
    capabilities=[TextSummaryCapability(), TextStatsCapability()]
)
