# Architecture

The Enterprise Brain is a knowledge boundary between source systems and an assistant. Its purpose is to preserve what a company knows, how it knows it and which uses are permitted.

## Responsibilities

| Layer | Responsibility | Must not imply |
| --- | --- | --- |
| Source adapters | Enumerate authorized items and identify observed versions | Permission to read an entire connected account |
| Extraction | Produce excerpts with source locators and coverage limits | That extracted claims are true or approved |
| Reconciliation | Link entities, find overlaps and surface contradictions | That text similarity establishes identity or authority |
| Review | Inspect evidence and accept an exact change | Approval of future revisions |
| Knowledge layer | Maintain typed records, ownership, validity and evidence | That every stored record is current |
| Retrieval | Filter permitted records, then select bounded context | That relevant text is safe or authoritative |
| Agent interface | Return evidence or accept scoped change proposals | Permission to execute arbitrary business actions |

The diagram in the README shows this design space. This repository implements only a tiny read path over bundled synthetic records. It does not contain a connector service, ingestion worker, vector store, MCP transport or hosted backend.

## A question through the demo

1. Match the question to an explicit synthetic topic. There are no embeddings or model calls.
2. Filter the topic by domain and the simulated audience before selecting records.
3. Require exactly one approved decision valid at the requested date.
4. Verify each cited local file against the fingerprint recorded at fixture construction.
5. Return decision fields, supporting locators and the distinction between draft and accepted outcome.
6. Abstain on missing context, conflicting authority or evidence that changed.

The default date is fixed at 2026-10-20 so the example is reproducible. It is not a claim about today's company state. Dates outside the decision's validity interval produce no answer.

## Design tradeoffs

Readable files make review and debugging accessible. Typed metadata makes deterministic filtering possible. They do not solve concurrent editing, distributed authorization or semantic interpretation by themselves.

A larger system could use a search index as a derived projection while retaining reviewed records and source references as authority. Index regeneration should not silently change approval or overwrite conflicting knowledge. No particular database or retrieval engine is required by this showcase.

## Evaluation questions

Useful future experiments would measure citation correctness, unsupported-answer rate, conflict detection, update latency and permission leakage. They would compare document-only retrieval with reviewed structured context using a held-out synthetic question set. This repository reports no benchmark results; its tests check specific failure cases, not general retrieval accuracy.
