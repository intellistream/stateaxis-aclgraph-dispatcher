# stateaxis-aclgraph-dispatcher

Extension ID: `org.vllm-hust.stateaxis-aclgraph-dispatcher`

Descriptor and capability-governed ACLGraph dispatch with fail-closed eager fallback.

This repository is the independent MOD boundary for StateAxis issues [#6](https://github.com/Qixin-Gaoke/stateaxis/issues/6), [#67](https://github.com/Qixin-Gaoke/stateaxis/issues/67).
It is deliberately `import_only`, default-off, and cannot be enabled. The split does
not inherit correctness, device, performance, or publication qualification from the
aggregate StateAxis repository.

## Evidence boundary

Status: **negative**.

Qwen B1–B32 authority and exactness passed; throughput regressed 0.324%, so no material end-to-end benefit is claimed.

The copied evidence and its SHA-256 are recorded in `PROVENANCE.json`. Negative,
failed, and inconclusive results are retained. Microbenchmarks and component results
must not be restated as online end-to-end gains.

## Install and inspect

```bash
python -m pip install .
vllm-hust-ext extension inspect org.vllm-hust.stateaxis-aclgraph-dispatcher
vllm-hust-ext extension check org.vllm-hust.stateaxis-aclgraph-dispatcher
```

Discovery does not enable the MOD. A future active revision must extract an
independently reviewable implementation, declare exclusive resources where needed,
and pass exactness, lifecycle, release, failure-recovery, and matched real-online
gates.

## Validate

```bash
python -m pip install -e '.[test]'
pytest -q
```

Maintainer: Shuhao Zhang (Tony), directly responsible; no advisor is declared.
