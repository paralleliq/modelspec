<div align="center">
  <img src="images/company-logo.png" alt="Paralleliq Logo" width="300"/>
</div>

<h1 align="center">ModelSpec</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Version-v0.1-blue.svg?style=flat-square">
  <img src="https://img.shields.io/badge/Category-AI%20Infrastructure-lightgrey.svg?style=flat-square">
  <img src="https://img.shields.io/badge/License-Apache%202.0-orange.svg?style=flat-square">
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square">
</p>

<p align="center">
  <strong>A declarative standard for describing what an AI model needs to run — and how it should behave in production.</strong>
</p>

---

## The problem

When a model moves from development to production, critical knowledge gets lost:

- What GPU does it actually need?
- What's the max batch size before latency degrades?
- How many replicas does it need at peak?
- What compliance rules apply to its inputs and outputs?

This knowledge lives in someone's head, a Slack thread, or a runbook nobody reads. When something breaks at 2am, nobody knows what "correct" looks like.

**ModelSpec makes this knowledge explicit, machine-readable, and version-controlled.**

---

## What it looks like

A minimal ModelSpec — model identity and GPU requirement:

```yaml
apiVersion: piqc.ai/v1alpha1
kind: ModelSpec

metadata:
  name: minimal-llm

spec:
  identity:
    model:
      id: example-llm
      family: llama
      task: text-generation
      framework: transformers

  runtime:
    accelerator:
      vendor: nvidia
      type: a10
      count: 1
```

A production ModelSpec — full operational contract:

```yaml
apiVersion: piqc.ai/v1alpha1
kind: ModelSpec

metadata:
  name: llama-2-70b-chat-prod
  version: "2025-01"
  description: Production chat LLM for customer support
  labels:
    team: ml-platform
    environment: prod

spec:
  identity:
    model:
      id: llama-2-70b-chat
      family: llama-2
      task: chat-completion
      framework: vllm
      precision: fp16

  runtime:
    accelerator:
      vendor: nvidia
      type: a100-80gb
      count: 4
    batch:
      maxBatchSize: 64
      maxSequenceLengthTokens: 4096

  operations:
    serving:
      protocol: http
      port: 8000
      maxConcurrency: 32
      timeoutSeconds: 60

    scaling:
      minReplicas: 2
      maxReplicas: 10
      targetLatencyMsP95: 800
      targetRps: 50

  governance:
    compliance:
      pii:
        allowed: false
        policy: internal-pii-policy-v3
      retention:
        logsDays: 30
```

---

## What ModelSpec captures

| Section | What it declares |
|---|---|
| `identity` | Model family, task, framework, precision, artifact locations |
| `runtime` | GPU type, count, batch limits, sequence length, memory |
| `operations.serving` | Protocol, port, concurrency, health probes, timeouts |
| `operations.scaling` | Min/max replicas, latency targets, RPS targets |
| `operations.observability` | Metrics, logging, tracing expectations |
| `pipeline` | Dependencies — guardrails, embeddings, RAG components |
| `governance` | PII policy, data retention, compliance rules |

Not all fields are required. ModelSpec is designed to grow with your deployment's maturity.

---

## Quick start

### Validate a ModelSpec

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r tooling/validator/requirements.txt

python tooling/validator/validate.py --schema schema/modelspec.v0.1.json examples/
```

### Explore the examples

The `examples/` directory has a progressive set of specs from minimal to full production:

| Example | What it adds |
|---|---|
| `00-minimal` | Model identity + GPU requirement |
| `01-artifacts` | Weight and tokenizer locations |
| `02-serving` | HTTP interface, health probes |
| `03-batching` | Batch size and sequence constraints |
| `04-scaling` | Replica targets, latency SLOs |
| `05-observability` | Metrics, logs, tracing |
| `06-dependencies-rag` | RAG pipeline with model dependencies |
| `07-governance-minimal` | PII policy, data retention |
| `08-full-production` | Complete production contract |

Start with `00` and work down — each example builds on the previous one.

---

## Where ModelSpec fits

ModelSpec is one layer in a three-part system:

```
Knowledge Base   — what should be true (best practices, GPU compatibility)
ModelSpec        — what was intended (declared model contract)          ← this repo
piqc scan        — what is actually running (runtime inspection)
```

Used alone, ModelSpec is a documentation and validation standard. Paired with [piqc](https://github.com/paralleliq/piqc), it becomes the basis for detecting drift between what a model was declared to need and what it's actually running on.

---

## Repository layout

```
schema/       — ModelSpec JSON schema (v0.1)
examples/     — Validated example ModelSpecs (00 through 08)
tooling/      — Validator and supporting tools
docs/         — Versioning guide and reference documentation
```

---

## Contributing

ModelSpec is an open standard. Contributions are welcome — new fields, new examples, validator improvements, or corrections.

1. Read the [Contributing Guide](CONTRIBUTING.md)
2. Check open [Issues](https://github.com/paralleliq/modelspec/issues)
3. Join the discussion on [GitHub Discussions](https://github.com/paralleliq/modelspec/discussions)

---

## Versioning

This repository targets **ModelSpec v0.1** (v1alpha1). See the [versioning guide](docs/v0.1/versioning.md) for schema version and compatibility details.

---

## License

Apache License 2.0 — see [LICENSE](LICENSE) for details.

---

<div align="center">
  <sub>Built by <a href="https://paralleliq.ai">Paralleliq</a> · <a href="mailto:info@paralleliq.ai">info@paralleliq.ai</a></sub>
</div>
