# StateAxis ACLGraph Dispatcher

Extension ID: `org.vllm-hust.stateaxis-aclgraph-dispatcher`

This MOD owns the bounded activation contract for StateAxis issues
[#6](https://github.com/Qixin-Gaoke/stateaxis/issues/6) and
[#67](https://github.com/Qixin-Gaoke/stateaxis/issues/67). The mechanism makes
one versioned descriptor/capability decision per Qwen2 dense BF16 decode batch,
uses ACLGraph only for admitted B1-B32 shapes with stable addresses, falls back
to eager execution for known unsupported cases, and fails closed on malformed
or stale identity.

## Activation

The default remains eager ACLNN. The candidate can be enabled only through the
vLLM-HUST Extension Manager/ECPA Manifest 0.3 `additional_config`; StateAxis
rejects direct ambient `STATE_ENGINE_ONLINE_DECODE_EXECUTION` activation. The
validated host then derives the worker-local execution policy and records the
MOD identity in the assembly fingerprint.

```bash
python -m pip install .
vllm-hust-ext extension inspect org.vllm-hust.stateaxis-aclgraph-dispatcher
VLLM_HUST_EXT_CONFIG=evidence/ecpa-contract-20261011/manager-config.json \
  vllm-hust-ext extension check org.vllm-hust.stateaxis-aclgraph-dispatcher
VLLM_HUST_EXT_CONFIG=evidence/ecpa-contract-20261011/manager-config.json \
  vllm-hust-ext extension plan org.vllm-hust.stateaxis-aclgraph-dispatcher
VLLM_HUST_EXT_CONFIG=evidence/ecpa-contract-20261011/manager-config.json \
  vllm-hust-ext run --dry-run -- /path/to/native_state_engine
```

## Evidence boundary

The retained 2026-08-16 Qwen2.5-14B BF16 3+3 matched run was token-exact and
lifecycle-clean, with 279 decisions per candidate run, zero fallback/rebuild,
and a 0.324% request-throughput regression. This is a negative result for that
cell, not a claim that graphs cannot help other architectures or workloads.

The 2026-10-11 revision proves the active ECPA contract, hash binding, assembly
identity separation, C++ decision contract, full worker build, and direct-env
rejection. It does not contain a fresh real-online run for the new host/MOD
identity, so no current performance claim is made.

See [EVIDENCE.md](EVIDENCE.md) and
[`RESULT.json`](evidence/ecpa-contract-20261011/RESULT.json).

## Validate

```bash
python -m pip install -e '.[test]'
ruff check .
ruff format --check .
pytest -q
python -m build
```

Maintainer: Shuhao Zhang (Tony), directly responsible; no advisor is declared.
