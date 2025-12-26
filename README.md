# ModelSpec

**ModelSpec** is an open, declarative specification for describing AI and LLM models, their runtime requirements, and their operational expectations. It is designed to make **model intent explicit** — independently of how or where a model is deployed.

---

## Why ModelSpec

Modern AI systems fail less often because of model quality and more often because of **implicit assumptions**:

- hardware constraints are undocumented  
- batching and sequence limits are guessed  
- scaling targets are unclear  
- observability expectations are inconsistent  
- governance policies are abstract, not operational  

ModelSpec exists to capture these assumptions in a **machine-readable, human-auditable format**.

---

## What ModelSpec Is (and Is Not)

**ModelSpec is:**

- declarative (describes intent, not actions)  
- runtime- and platform-agnostic  
- focused on individual models and their expectations  
- suitable for documentation, validation, and analysis  

**ModelSpec is not:**

- a deployment tool  
- an orchestration engine  
- a scheduler  
- a policy enforcement system  

Those concerns are intentionally out of scope.

---

## Core Concepts

A ModelSpec describes:

- **Model identity** – model family, task, framework, precision  
- **Artifacts** – weights, tokenizer, versioned sources  
- **Runtime requirements** – accelerator type, batch and sequence constraints  
- **Operational contracts** – serving interface, scaling targets  
- **Observability expectations** – metrics, logs, traces (what must exist)  
- **Dependencies** – relationships to other models (e.g. RAG components)  
- **Governance constraints** – data handling, retention, compliance rules  

Not all fields are required. ModelSpec is designed to grow with maturity.

---

## Learning Path

This repository includes a **progressive set of examples** under the `examples/` directory:

| Example | Focus                                 |
|---------|---------------------------------------|
| 00      | Minimal ModelSpec (identity + GPU)    |
| 01      | Model artifacts                       |
| 02      | Serving interface                     |
| 03      | Batching & sequence constraints       |
| 04      | Scaling targets                       |
| 05      | Observability expectations            |
| 06      | Model dependencies (RAG pattern)      |
| 07      | Minimal governance                    |
| 08      | Full production example (advanced)    |

New users should start with **00** and move downward, as each example builds on the previous one.

---

## Relationship to PIQC

ModelSpec is part of a broader ecosystem within ParallelIQ:

- **Knowledge Base** — what *should* be true (best practices, policies)  
- **ModelSpec** — what was *intended* (declared model contract)  
- **PIQC Scan** — what is *actually running* (runtime inspection)  

ModelSpec can be used independently, but becomes more powerful when paired with runtime inspection and analysis tools like PIQC Scan.

---

## Versioning

This repository currently targets **ModelSpec v0.1** (v1alpha1). See the [Versioning guide](docs/versioning.md) for details on schema versions and compatibility.
