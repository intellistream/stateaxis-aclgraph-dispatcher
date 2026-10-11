# Active ECPA contract — 2026-10-11

This directory records activation and build validation for release `0.2.0`.
The StateAxis host at `8e4627bb6d1ad14fc953e6ed0926289df065652b`
accepts only the exact research-manifest digest through ECPA, fingerprints the
MOD identity into the assembly, rejects direct ambient decode-policy
activation, and derives the worker-local ACLGraph policy after validation.

The historical 3+3 real-NPU result is retained separately and remains negative
for its tested Qwen2.5-14B cell. No fresh online run was made for this new
host/MOD identity, so the current release is not performance-qualified.
