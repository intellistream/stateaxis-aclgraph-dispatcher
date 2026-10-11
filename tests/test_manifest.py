import hashlib
import json
from pathlib import Path

import pytest
from vllm_hust_ext.manifest import activation_blocker, load_manifest

import stateaxis_aclgraph_dispatcher
from stateaxis_aclgraph_dispatcher import (
    AclGraphDispatcherConfig,
    aclgraph_dispatcher,
)


def test_manifest_is_active_and_hash_bound() -> None:
    package = Path(stateaxis_aclgraph_dispatcher.__file__).parent
    repo = package.parents[1]
    path = package / "vllm-hust-extension-v0.3.json"
    manifest = load_manifest(path)
    assert manifest.bundle_id == "org.vllm-hust.stateaxis-aclgraph-dispatcher"
    assert manifest.schema_version == "0.3-experimental"
    assert activation_blocker(manifest) is None
    raw = json.loads(path.read_text())
    expected = raw["activation"]["additional_config"]["stateaxis_mod"][
        "manifest_sha256"
    ]
    actual = hashlib.sha256((repo / "RESEARCH_MANIFEST.json").read_bytes()).hexdigest()
    assert actual == expected


def test_contract_is_qwen2_decode_bound_and_fail_closed() -> None:
    assert aclgraph_dispatcher() == AclGraphDispatcherConfig()
    with pytest.raises(ValueError, match="reviewed contract"):
        AclGraphDispatcherConfig(sampling_fallback_to_eager=False)
