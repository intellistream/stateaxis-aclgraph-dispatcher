# Historical R3 matched real-NPU result

This is the accepted StateAxis issue #67 campaign: Qwen2.5-14B BF16, physical
Ascend 910B2 NPU3, 128 independent-cold requests, concurrency 32, 32 output
tokens, and three fresh processes per arm in interleaved order.

| Metric | Control median | Candidate median | Delta |
|---|---:|---:|---:|
| Request throughput | 2.995329 req/s | 2.985617 req/s | -0.324% |
| Output-token throughput | 95.850530 tok/s | 95.539746 tok/s | -0.324% |
| TTFT P50 | 8,675.028 ms | 8,678.994 ms | +0.046% |
| TTFT P95 | 13,595.079 ms | 13,621.404 ms | +0.194% |
| TPOT P50 | 37.730 ms | 38.501 ms | +2.043% |
| TPOT P95 | 70.889 ms | 64.957 ms | -8.369%; noisy |
| Peak HBM | 58,567 MiB | 58,573 MiB | +6 MiB |

All six runs were token-exact and lifecycle-clean. Every candidate run applied
279 decisions, captured two graph buckets, replayed 279 times, and reported zero
fallback and zero rebuild; every control dispatcher counter remained zero. This
proves the treatment was active rather than an inert ON arm.

The paired request-throughput deltas were -0.491%, -1.025% and -0.085%. Their
post-hoc mean is -0.534%, with a two-sided 95% Student-t interval of
[-1.704%, +0.637%]. This exploratory interval was not the preregistered decision
statistic and must not be retroactively used as a significance claim. Together with
the stable median result it supports only “no material benefit in this frozen cell.”

Eager ACLNN therefore remained the default. The result does not invalidate graph
execution for different model architectures, sampling support, batch distributions,
stable-address regimes or a later MOD/host identity. The active ECPA revision needs
its own matched real-NPU campaign before inheriting any performance classification.
