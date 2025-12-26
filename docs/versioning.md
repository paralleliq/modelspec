# ModelSpec v0.1 – Required vs Optional Fields

This document provides a quick reference for fields in the ModelSpec schema (v0.1), indicating which fields are required and which are optional.

## Top-Level Fields (Required)

| Field              | Requirement | Notes                                |
| ------------------ | ----------- | ------------------------------------ |
| apiVersion         | Required    | Must be `piqc.ai/v1alpha1`           |
| kind               | Required    | Must be `ModelSpec`                  |
| metadata.name      | Required    | Unique model identifier              |
| spec.identity.model | Required   | Model identity block                 |
| spec.runtime.accelerator | Required | Hardware accelerator specification |

## Identity Section

**Required fields:**

| Path                         | Description                              |
| ---------------------------- | ---------------------------------------- |
| spec.identity.model.id       | Model ID (e.g., `llama-2-70b-chat`)       |
| spec.identity.model.family   | Model family (e.g., `llama-2`)            |
| spec.identity.model.task     | Primary task (e.g., `chat`, `embedding`)  |
| spec.identity.model.framework | Serving framework (e.g., `vllm`, `TGI`)  |

**Optional fields:**

| Path                              | Description                              |
| --------------------------------- | ---------------------------------------- |
| metadata.version                  | Version string for this spec             |
| metadata.description              | Human-readable description               |
| metadata.labels.*                 | Arbitrary key-value labels               |
| metadata.annotations.*            | Arbitrary key-value annotations          |
| spec.identity.model.precision     | Numerical precision (e.g., `fp16`, `int8`) |
| spec.identity.model.artifacts.modelUri      | URI or path to model weights      |
| spec.identity.model.artifacts.tokenizerUri  | URI or path to tokenizer data     |

## Runtime Section

**Required fields:**

| Path                                | Description                              |
| ----------------------------------- | ---------------------------------------- |
| spec.runtime.accelerator.vendor     | Accelerator vendor (e.g., `nvidia`)      |
| spec.runtime.accelerator.type       | Accelerator type/model (e.g., `A100-80GB`) |
| spec.runtime.accelerator.count      | Number of accelerators (minimum 1)       |

**Optional fields:**

| Path                                       | Description                         |
| ------------------------------------------ | ----------------------------------- |
| spec.runtime.batch.maxBatchSize            | Maximum batch size                  |
| spec.runtime.batch.maxSequenceLengthTokens | Maximum sequence length (tokens)    |
| spec.runtime.resources.cpuCores            | CPU cores allocated                 |
| spec.runtime.resources.memoryGb            | Memory (in GB) allocated            |
| spec.runtime.resources.ephemeralStorageGb  | Ephemeral storage (in GB)           |
| spec.runtime.environment.variables         | Environment variables map           |

## Operations Section

_All fields in `operations` are optional. Key areas include:_

- **serving:** `protocol`, `port`, `readinessProbe`, `livenessProbe`, `maxConcurrency`, `timeoutSeconds`  
- **scaling:** `minReplicas`, `maxReplicas`, `strategy`, `targetLatencyMsP95`, `targetRps`, `warmPool`  
- **observability:** `metrics` (enabled, provider, port), `logging` (level), `tracing` (enabled flag)  

## Pipeline Section

_All fields in `pipeline` are optional. This section describes how the model integrates into a larger pipeline:_

- **preprocess:** an ordered list of preprocessing steps (if any)  
- **postprocess:** an ordered list of postprocessing steps (if any)  
- **dependencies:** other models or components this model relies on (each dependency has an `id`, `role`, and interface parameters)  

## Governance Section

_All fields in `governance` are optional. This section captures compliance and cost constraints:_

- **compliance:** policies for PII handling (`allowed`, `policy`) and data retention (`logsDays`, `artifactsDays`); may also include change approval processes or owner information  
- **cost:** cost targets (e.g., `targetCostPer1kTokensUsd`) and pricing hints (cloud provider, instance type, spot instance allowance)  

---

**Summary:** A minimal valid ModelSpec requires only the model identity and the accelerator specification. All other fields enhance optimization, integration, operations, or governance. This keeps onboarding simple while allowing advanced teams full expressiveness as needed.
