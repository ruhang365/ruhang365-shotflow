"""Provider metadata and validation.

ShotFlow does not submit generation jobs. Adapters describe portable settings
and whether a configuration has been forward-tested by the project.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ProviderAdapter:
    adapter_id: str
    display_name: str
    verified_models: tuple[str, ...]
    parameter_names: tuple[str, ...]

    def validate(self, model: str, parameters: dict[str, Any]) -> list[str]:
        problems: list[str] = []
        unknown = sorted(set(parameters) - set(self.parameter_names))
        if unknown:
            problems.append(
                f"Unsupported parameters for {self.adapter_id}: {', '.join(unknown)}"
            )
        if model not in self.verified_models:
            problems.append(
                f"Model {model!r} is not verified for {self.adapter_id}; "
                "keep verified=false until real evidence exists"
            )
        return problems


SEEDANCE_2 = ProviderAdapter(
    adapter_id="seedance-2.0",
    display_name="Seedance 2.0",
    verified_models=("seedance2.0_vision",),
    parameter_names=("ratio", "resolution", "duration_seconds"),
)

GENERIC = ProviderAdapter(
    adapter_id="generic",
    display_name="Generic AI video provider",
    verified_models=(),
    parameter_names=("ratio", "resolution", "duration_seconds"),
)

ADAPTERS = {
    GENERIC.adapter_id: GENERIC,
    SEEDANCE_2.adapter_id: SEEDANCE_2,
}


def get_adapter(adapter_id: str) -> ProviderAdapter:
    try:
        return ADAPTERS[adapter_id]
    except KeyError as exc:
        raise ValueError(
            f"Unknown provider adapter {adapter_id!r}. "
            f"Available adapters: {', '.join(sorted(ADAPTERS))}"
        ) from exc
