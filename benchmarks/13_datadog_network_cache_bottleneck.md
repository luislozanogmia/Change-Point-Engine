# Benchmark 13: datadog_network_cache_bottleneck

This report preserves the benchmark comparison format used during the research run. It contains public-case input only, generated trace output, isolated baseline response, isolated trace-on response, and the review verdict.

## Normalized Engine Input

```text
timestamp,service,metric,value
baseline,c14_datadog_network_cache_bottleneck,p99_remote_cache_latency_ms,100.0
incident,c14_datadog_network_cache_bottleneck,p99_remote_cache_latency_spike_ms,1000.0
envoy_cpu_limit,c14_datadog_network_cache_bottleneck,cpu_allocation_cores,2.0
after_envoy_cpu,c14_datadog_network_cache_bottleneck,p99_latency_lower_ms,300.0
after_envoy_cpu,c14_datadog_network_cache_bottleneck,p99_latency_upper_ms,1000.0
ena_bug,c14_datadog_network_cache_bottleneck,transmit_queues_used_bug_count,1.0
ena_bug,c14_datadog_network_cache_bottleneck,transmit_queues_available_count,8.0
after_ena_hotfix,c14_datadog_network_cache_bottleneck,p99_latency_lower_ms,200.0
after_ena_hotfix,c14_datadog_network_cache_bottleneck,p99_latency_upper_ms,600.0
after_network_optimized_instances,c14_datadog_network_cache_bottleneck,p99_latency_typical_ms,100.0
after_network_optimized_instances,c14_datadog_network_cache_bottleneck,occasional_spike_latency_ms,1000.0
after_prestop_hook,c14_datadog_network_cache_bottleneck,p99_remote_cache_latency_upper_ms,100.0
post_resolution,c14_datadog_network_cache_bottleneck,remote_cache_scale_down_factor_x,6.0
```

## Baseline Prompt: Raw Input Only

```text
You are a fresh performance benchmark evaluator with zero prior context.

Analyze ONLY the public evidence below. Identify:
1. the performance issue,
2. the evidence,
3. the missing evidence,
4. the recommended next diagnostic step.

Do not invent root cause beyond the evidence.

CASE:
# c14 Datadog network/cache bottleneck

Source: https://www.datadoghq.com/blog/engineering/not-just-another-network-latency-issue/

Status: accepted

Raw performance evidence exists: yes. Datadog reports that the `counter` application normally saw p99 remote-cache round-trip latency around 100 ms, but during rollouts it spiked above 1 s and caused excessive-backlog pages. The post also documents intermediate post-fix latency bands of 300 ms-1 s and 200-600 ms.

Resolution evidence exists: yes. Datadog describes staged fixes: allocating more CPU to Envoy, patching a Linux ENA transmit-queue bug, moving to network-optimized EC2 instances, and implementing a Kubernetes preStop hook plus Envoy client behavior to avoid terminating cache pods. After the final change, p99 latency consistently fell below 100 ms.

Normalization: feasible from visible numeric latency bands and infrastructure counts. `normalized.csv` captures each investigation/fix stage.

RAW EVIDENCE:
Public source: https://www.datadoghq.com/blog/engineering/not-just-another-network-latency-issue/

Relevant raw performance evidence:

- Datadog's `counter` app fetches data from a remote cache during startup; while the local cache populates, requests process at a much slower rate.
- Normal p99 remote-cache latency is around 100 ms.
- During rollouts, p99 remote-cache latency spiked upward of 1 second, producing excessive-backlog pages.
- Network Performance Monitoring showed TCP retransmits spiking during each `counter` deployment.
- The Envoy sidecar maxed out its CPU allocation of two cores and was throttled.
- After more Envoy CPU was added, production latency still oscillated between 300 ms and 1 s during rollouts.
- A Linux kernel bug mapped traffic to the first ENA transmit queue instead of across eight transmit queues.
- After the ENA hotfix, non-rollout spikes improved, but rollout latency still oscillated between 200 ms and 600 ms.
- High AWS ENA bandwidth allowance exceeded metrics indicated dropped packets at the hypervisor level.
- After migrating to network-optimized EC2 instances, latency mostly hovered around 100 ms but still had occasional 1 s spikes.
- Final spikes correlated with terminating remote-cache pods and one-second timeouts/retries.

Return concise structured findings.
```

## Baseline Response

```text
1. Performance issue
Datadog's `counter` service suffered rollout-time remote-cache latency spikes that slowed startup processing and produced excessive-backlog pages.

2. Evidence
- Normal p99 remote-cache round-trip latency was about 100 ms.
- During rollouts, p99 latency rose above 1 second.
- TCP retransmits spiked during each `counter` deployment.
- Envoy sidecars maxed out their two-core CPU allocation and were throttled.
- After adding Envoy CPU, rollout latency still oscillated between 300 ms and 1 s.
- A Linux ENA transmit-queue bug concentrated traffic on the first of eight queues.
- After the ENA hotfix, non-rollout spikes improved, but rollout latency still oscillated between 200 ms and 600 ms.
- ENA bandwidth allowance exceeded metrics showed hypervisor-level packet drops.
- Network-optimized EC2 instances reduced latency mostly to about 100 ms, but occasional 1 s spikes remained.
- Final spikes correlated with terminating remote-cache pods and one-second timeout/retry behavior.

3. Missing evidence
- Exact request rates, cache hit/miss ratios, and backlog depth during each rollout phase.
- Per-hop latency and packet-loss attribution across app, Envoy, node, and AWS network layers.
- Kernel, ENA driver, and EC2 instance details for affected nodes.
- Quantified effect of the final preStop/client-behavior change.

4. Recommended next diagnostic step
Build a rollout-correlated timeline joining p99 cache latency, TCP retransmits, Envoy throttling, ENA drops, pod termination events, and retry counts to isolate which bottleneck remains active at each phase.
```

## Trace-On Prompt: Raw Input Plus Change Trace

```text
You are a fresh performance benchmark evaluator with zero prior context.

Analyze ONLY the public evidence and precomputed deterministic trace below. Identify:
1. the performance issue,
2. the evidence,
3. the missing evidence,
4. the recommended next diagnostic step.

Use the trace as structured evidence. Do not treat it as root-cause proof.
Do not invent root cause beyond the evidence.

CASE:
# c14 Datadog network/cache bottleneck

Source: https://www.datadoghq.com/blog/engineering/not-just-another-network-latency-issue/

Status: accepted

Raw performance evidence exists: yes. Datadog reports that the `counter` application normally saw p99 remote-cache round-trip latency around 100 ms, but during rollouts it spiked above 1 s and caused excessive-backlog pages. The post also documents intermediate post-fix latency bands of 300 ms-1 s and 200-600 ms.

Resolution evidence exists: yes. Datadog describes staged fixes: allocating more CPU to Envoy, patching a Linux ENA transmit-queue bug, moving to network-optimized EC2 instances, and implementing a Kubernetes preStop hook plus Envoy client behavior to avoid terminating cache pods. After the final change, p99 latency consistently fell below 100 ms.

Normalization: feasible from visible numeric latency bands and infrastructure counts. `normalized.csv` captures each investigation/fix stage.

RAW EVIDENCE:
Public source: https://www.datadoghq.com/blog/engineering/not-just-another-network-latency-issue/

Relevant raw performance evidence:

- Datadog's `counter` app fetches data from a remote cache during startup; while the local cache populates, requests process at a much slower rate.
- Normal p99 remote-cache latency is around 100 ms.
- During rollouts, p99 remote-cache latency spiked upward of 1 second, producing excessive-backlog pages.
- Network Performance Monitoring showed TCP retransmits spiking during each `counter` deployment.
- The Envoy sidecar maxed out its CPU allocation of two cores and was throttled.
- After more Envoy CPU was added, production latency still oscillated between 300 ms and 1 s during rollouts.
- A Linux kernel bug mapped traffic to the first ENA transmit queue instead of across eight transmit queues.
- After the ENA hotfix, non-rollout spikes improved, but rollout latency still oscillated between 200 ms and 600 ms.
- High AWS ENA bandwidth allowance exceeded metrics indicated dropped packets at the hypervisor level.
- After migrating to network-optimized EC2 instances, latency mostly hovered around 100 ms but still had occasional 1 s spikes.
- Final spikes correlated with terminating remote-cache pods and one-second timeouts/retries.

PRECOMPUTED CHANGE TRACE:
--- CHANGE TRACE ---
This trace surfaces evidence and candidate explanations. It does not decide root cause.

DETECTOR ROUTE:
  Data shape: benchmark_condition_table
  Selected detectors: condition_delta
  Evidence: 9 condition labels across 13 rows; treat rows as benchmark conditions, not continuous incident time

SIGNAL BLOCKS:
  [1] phased_remediation: c14_datadog_network_cache_bottleneck.remote_cache_scale_down_factor_x at post_resolution, confidence=0.74
      Evidence: multiple after/post-remediation stages are present; preserve staged fixes and residual bottlenecks instead of collapsing to one before/after delta
  [2] mechanism_evidence: c14_datadog_network_cache_bottleneck.cpu_allocation_cores at envoy_cpu_limit, confidence=0.72
      Evidence: named low-level mechanisms appear in the evidence; retain them as evidence labels without promoting them to root cause unless backed by profiling, bisection, or owner notes
      mechanisms: envoy, ena, transmit_queues, prestop
  [3] condition_delta: c14_datadog_network_cache_bottleneck.p99_latency_lower_ms at after_envoy_cpu (200.0 -> 300.0), confidence=0.66
      Evidence: p99_latency_lower_ms changes across benchmark conditions; min=200 at after_ena_hotfix; max=300 at after_envoy_cpu; ratio=1.50x; compare conditions before explaining cause
  [4] condition_delta: c14_datadog_network_cache_bottleneck.p99_latency_upper_ms at after_envoy_cpu (600.0 -> 1000.0), confidence=0.7
      Evidence: p99_latency_upper_ms changes across benchmark conditions; min=600 at after_ena_hotfix; max=1000 at after_envoy_cpu; ratio=1.67x; compare conditions before explaining cause
  [5] config_expansion: c14_datadog_network_cache_bottleneck.remote_cache_scale_down_factor_x at post_resolution, confidence=0.78
      Evidence: remote_cache_scale_down_factor_x is 6x, indicating a material expansion/change in generated configuration

CANDIDATE CASCADES:
  No cross-service timing cascade detected.

OPTIONS FOR THE LLM TO WEIGH:
  Option A: c14_datadog_network_cache_bottleneck.remote_cache_scale_down_factor_x is the first visible shift.
  Option C: this is sparse benchmark evidence; preserve condition labels and deltas.
  Option C: preserve named mechanisms as evidence labels, not automatic root cause.
  Option D: detector output is incomplete; request more metrics if evidence is thin.

GUARDRAIL:
  Do not turn timing into causality without dependency, deploy, or resource evidence.

Return concise structured findings.
```

## Trace-On Response

```text
## 1. Performance Issue

Rollout-sensitive remote-cache latency spikes in Datadog's `counter` application. During deployments, p99 remote-cache round-trip latency rises well above the normal ~100 ms level, producing backlog pages and requiring staged remediation.

## 2. Evidence

- Normal p99 remote-cache latency is around 100 ms.
- During rollouts, p99 latency spikes upward of 1 second.
- Network Performance Monitoring shows TCP retransmits spiking during each `counter` deployment.
- Envoy sidecar CPU reached its two-core allocation and was throttled.
- After adding Envoy CPU, rollout latency still oscillated between 300 ms and 1 s.
- After an ENA transmit-queue hotfix, non-rollout spikes improved, but rollout latency still oscillated between 200 ms and 600 ms.
- Bandwidth allowance exceeded metrics indicated dropped packets at the hypervisor level.
- Moving to network-optimized EC2 instances reduced latency near 100 ms but left occasional 1 s spikes, later correlated with terminating remote-cache pods and one-second timeouts/retries.
- The trace highlights staged remediation, so the evidence should not be collapsed into a single root cause.

## 3. Missing Evidence

- Full time series for latency, retransmits, Envoy throttling, ENA drops, and rollout events.
- Per-stage before/after sample sizes and variance.
- Packet captures or flow-level evidence tying retransmits/drops directly to cache request latency.
- Quantified contribution of terminating cache pods versus network bottlenecks.
- Application backlog depth and request processing rate during each stage.

## 4. Recommended Next Diagnostic Step

Build a rollout-aligned timeline that overlays p99 cache latency, TCP retransmits, Envoy CPU throttling, ENA bandwidth/drop metrics, cache pod termination events, and backlog depth. Use it to separate the network-capacity stages from the final pod-termination timeout path.
```

## Verdict Review

```text
Winner: similar

Reason: Both outputs identify rollout-sensitive remote-cache latency and staged remediation. Baseline preserves one extra concrete mechanism detail, the ENA transmit-queue imbalance, while trace-on better enforces the trace warning not to collapse the phases into a single root cause.

Engine action: Keep phased-remediation detection, but improve evidence retention for named low-level mechanisms within each phase, such as Envoy CPU throttling, ENA queue imbalance, hypervisor drops, and pod-termination retry behavior.
```
