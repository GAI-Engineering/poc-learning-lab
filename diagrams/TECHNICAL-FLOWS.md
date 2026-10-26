<img src="../assets/gai-observe-logo.png" alt="GAI Observe LLC" width="140">

# Technical Flows — POC Learning Lab
▸ GAI OBSERVE LLC · POC LEARNING LAB — execution order, 2026-10-26
*The companion to CONCEPT-DIAGRAMS.md: those show what the concepts ARE
(context); these show what RUNS, in what order (execution). Design rule
for the whole lab: the shortest honest pipeline — one pass, no hidden
state, standard library only.*

## 01 · sees.py — execution order
```mermaid
flowchart TD
    A["1 · Load 3 synthetic scenes<br/>(regions + ground truth)"]:::proc --> B["2 · For each region, emit a claim<br/>object + confidence"]:::proc
    B --> C{"3 · Classify<br/>confidence >= 0.60"}:::decision
    C -->|yes| D["GROUNDED"]:::proc
    C -->|no| E["GUESS"]:::warn
    D --> F["4 · Verification lookup<br/>scripted table in the demo"]:::proc
    E --> F
    F --> G["5 · Count survived, compute rate<br/>print JSON + write claims.csv"]:::metric
    classDef proc fill:#E6F4F6,stroke:#1B9AAA,stroke-width:1.5px,color:#123B40;
    classDef decision fill:#FBF3D9,stroke:#C9A227,stroke-width:2px,color:#5A4A00;
    classDef warn fill:#FBE9E7,stroke:#C1666B,stroke-width:1.5px,color:#6E2B26;
    classDef metric fill:#1B9AAA,stroke:#146B76,stroke-width:2px,color:#FFFFFF;
```
Simplicity notes: single pass over 13 regions; deterministic (same
input, same output, every run); the verification step is the ONLY part
that changes when a live model + human checkers replace the stub.

## 02 · conversation.py — execution order
```mermaid
flowchart TD
    A["1 · Load synthetic transactions"]:::proc --> B["2 · Analyst posts a question<br/>to the transcript"]:::proc
    B --> C["3 · Executor computes from data<br/>posts the answer to the transcript"]:::proc
    C --> D["4 · Findings pass<br/>executor posts what nobody asked"]:::proc
    D --> E["5 · Persist transcript (JSONL)<br/>the file IS the state"]:::metric
    E --> F["6 · Replay / audit<br/>read the file, nothing else exists"]:::proc
    classDef proc fill:#E6F4F6,stroke:#1B9AAA,stroke-width:1.5px,color:#123B40;
    classDef metric fill:#1B9AAA,stroke:#146B76,stroke-width:2px,color:#FFFFFF;
```
Simplicity notes: 12 messages total; agents share no memory — every
handoff is a transcript line, so the audit step (6) needs no tooling
beyond reading the file the run already wrote.

## 03 · rods_agent.py — execution order
```mermaid
flowchart TD
    A["1 · Parse the 4-line contract<br/>Role / Output / Do-Nots / Signal"]:::proc --> B{"2 · Lint, in order<br/>fields present -> output concrete -> signal typed"}:::decision
    B -->|any flag| X["STOP - the agent<br/>never executes"]:::warn
    B -->|CLEAN| C["3 · Run extraction<br/>over the clauses"]:::proc
    C --> D["4 · Emit obligations table<br/>+ EXTRACTION COMPLETE"]:::proc
    D --> E["5 · Termination check<br/>typed signal == contract Signal"]:::metric
    classDef proc fill:#E6F4F6,stroke:#1B9AAA,stroke-width:1.5px,color:#123B40;
    classDef decision fill:#FBF3D9,stroke:#C9A227,stroke-width:2px,color:#5A4A00;
    classDef warn fill:#FBE9E7,stroke:#C1666B,stroke-width:1.5px,color:#6E2B26;
    classDef metric fill:#1B9AAA,stroke:#146B76,stroke-width:2px,color:#FFFFFF;
```
Simplicity notes: the lint runs BEFORE any agent work and its order is
fixed — a contract fails at the first broken rule, so the fix is always
the earliest flag. Termination compares a typed signal, not text.
