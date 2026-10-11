"""ACLGraph dispatcher bounded activation contract."""

from __future__ import annotations

from dataclasses import asdict, dataclass

MOD_ID = "org.vllm-hust.stateaxis-aclgraph-dispatcher"


@dataclass(frozen=True, slots=True)
class AclGraphDispatcherConfig:
    """Exact Qwen2 BF16 decode capability and eager-fallback contract."""

    enabled: bool = True
    scope: str = "qwen2-dense-bf16-decode-b1-b32"
    descriptor_revision: int = 1
    capability_revision: int = 1
    execution_policy: str = "acl_graph_dispatcher"
    eager_default: bool = True
    sampling_fallback_to_eager: bool = True
    unsupported_fallback_to_eager: bool = True
    malformed_or_stale_fail_closed: bool = True
    state_mutation_before_capture: bool = True
    stable_addresses_required: bool = True
    decision_telemetry_required: bool = True
    fail_closed: bool = True

    def __post_init__(self) -> None:
        expected = {
            "enabled": True,
            "scope": "qwen2-dense-bf16-decode-b1-b32",
            "descriptor_revision": 1,
            "capability_revision": 1,
            "execution_policy": "acl_graph_dispatcher",
            "eager_default": True,
            "sampling_fallback_to_eager": True,
            "unsupported_fallback_to_eager": True,
            "malformed_or_stale_fail_closed": True,
            "state_mutation_before_capture": True,
            "stable_addresses_required": True,
            "decision_telemetry_required": True,
            "fail_closed": True,
        }
        if asdict(self) != expected:
            raise ValueError("ACLGraph dispatcher requires the reviewed contract")


def aclgraph_dispatcher() -> AclGraphDispatcherConfig:
    return AclGraphDispatcherConfig()


__all__ = ["MOD_ID", "AclGraphDispatcherConfig", "aclgraph_dispatcher"]
