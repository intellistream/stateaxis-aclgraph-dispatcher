# Issue #67 production ACLGraph dispatcher closure

> **Point-in-time closure report, not current repository status.** Current
> capability classification is owned by
> [`NATIVE_ENGINE_STATUS.md`](../../NATIVE_ENGINE_STATUS.md); immutable run detail is
> retained in the result directories named below.

## Scope and implementation

Issue #67 replaces the rejected fixed-shape #6 experiment boundary with a
versioned production dispatch decision. `NativeBatchDescriptor` and
`GraphCapability` bind model, dtype, layout, phase, batch size, stable-address,
sampling and state-mutation properties. The worker makes exactly one decision
per decode batch. Malformed or stale identity fails closed; a well-formed but
unsupported descriptor falls back to eager execution.

The public default remains `eager_aclnn`. The candidate is enabled only by
`STATE_ENGINE_ONLINE_DECODE_EXECUTION=acl_graph_dispatcher`. Its Qwen2.5-14B
BF16 execution plan binds an independent dispatcher contract SHA-256 and the
full B1--B32 graph mask. Sampling is intentionally unsupported by this
capability and therefore uses the eager fallback; state mutation/COW remains
admitted before capture.

Bounded telemetry records descriptor/capability revision, authority,
fallback reason, decisions, captures, replays and rebuilds. Unit tests cover
default-off behavior, supported authority, known-unsupported fallback and
malformed/stale fail-closed behavior. The official `.23` image built the full
C++ worker, and resident-plan, build-identity, dispatcher and native-protocol
tests passed without a device.

## Frozen identities and retained diagnostics

The local official image was
`quay.io/ascend/vllm-ascend:v0.23.0rc1-openeuler`, image ID
`sha256:f4c89c293e076453e9eef9edb5fb9669740dccbd3c48619a9f976d775fc29b81`.
The Rust bundle identity was
`d10c166090d3516a55570b50a942e24d3b4a1a737ec9dfcbb42f28dda3932578`.

- R1 is retained as a pre-worker failure: timing-v5 correctly rejected a
  contradictory device-event override. No arm ran.
- R2 disabled only that incompatible attribution option. Its aggregate
  identity is `7ecd9a3475a84beed935f30a258d2de24c8048b4ef3800e0449775f4f166147b`.
  The real NPU 1+1 was exact and lifecycle-clean; candidate applied 279
  dispatcher decisions with zero fallback and zero rebuild.
- R2 also performed the first full-byte verification under the canonical
  `/assets/repo` mount. R3 freezes the resulting 161-entry per-arm caches,
  keyed by canonical path, device, inode, size and nanosecond mtime plus the
  byte SHA. Any stat change still fails closed to a byte hash. R3 aggregate
  identity is
  `590ac068643e9d7cb46e335ab2d634a1dde9a3dd9fe8a4793124dcb16bc06633`.

The retained evidence is:

- `results/issue67-aclgraph-dispatcher-20260816-r1-1plus1/`;
- `results/issue67-aclgraph-dispatcher-20260816-r2-1plus1/`;
- `results/issue67-aclgraph-dispatcher-20260816-r3-3plus3/`.

## Matched real-NPU result

R3 ran on dynamically admitted physical NPU3. Both arms used the same model,
pack/oracle, state capacity 33, 272 cache blocks, 10 GiB workspace, B32
scheduler/decode capacity, 128 independent-cold requests, concurrency 32 and
32 output tokens. Every run was a fresh process; startup was excluded from the
matched HTTP request window. The order was control/candidate,
candidate/control, control/candidate.

All six runs were token-exact and lifecycle-clean. Every candidate run applied
279 decisions, captured two graph buckets, replayed 279 times, and reported
zero fallback and zero rebuild. All control dispatcher counters were zero.

| Metric | Control median | Candidate median | Candidate vs control |
|---|---:|---:|---:|
| Request throughput | 2.995329 req/s | 2.985617 req/s | -0.324% |
| Output-token throughput | 95.850530 tok/s | 95.539746 tok/s | -0.324% |
| TTFT p50 | 8675.028 ms | 8678.994 ms | +0.046% |
| TTFT p95 | 13595.079 ms | 13621.404 ms | +0.194% |
| TPOT p50 | 37.730 ms | 38.501 ms | +2.043% |
| TPOT p95 | 70.889 ms | 64.957 ms | -8.369% |
| Peak HBM | 58,567 MiB | 58,573 MiB | +6 MiB |

Request-throughput CV was 0.209% for control and 0.409% for candidate. TPOT
p95 was substantially noisier (6.11% and 12.43% CV), so its isolated decrease
does not establish a performance win against the stable throughput and p50
results.

## Classification

The dispatcher is functionally accepted as an identity-bound, fail-closed,
default-off production candidate. This matched workload shows **no material
end-to-end benefit** and a small throughput regression, so eager remains the
default. No speedup or vLLM/vLLM-HUST superiority claim is made. The result
does not invalidate future graph capabilities for different models, sampling
contracts or stable-address regimes; those require separately frozen evidence.
