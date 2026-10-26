<img src="../assets/gai-observe-logo.png" alt="GAI Observe LLC" width="140">

# Concept Diagrams — POC Learning Lab
▸ GAI OBSERVE LLC · POC LEARNING LAB — overview materials, 2026-10-26
*One diagram per POC: the concept on one screen. Mermaid source — renders
on GitHub, stays text in the repo (versionable, no binary drift). Palette:
navy = start/deliverable · teal = process · gold = decision · strong teal =
the headline idea · rose = the flagged path. Rendered versions of
the same three diagrams are a Day 2 deck item; the current deck
carries text flows.*

## 01 · An Agent That Sees — grounded perception + verification
```mermaid
flowchart LR
    A["Synthetic scene<br/>regions + ground truth"]:::io --> B["Parser emits claims<br/>region + confidence"]:::proc
    B --> C{"Confidence<br/>>= 0.60?"}:::decision
    C -->|yes| D["GROUNDED"]:::proc
    C -->|no| E["GUESS - flagged,<br/>not hidden"]:::warn
    D --> F["Verification<br/>vs ground truth"]:::proc
    E --> F
    F --> G["Survival rate<br/>survived / total"]:::metric
    G --> H["Confidence map<br/>the deliverable"]:::io
    classDef io fill:#1A1A2E,stroke:#C9A227,stroke-width:2px,color:#FFFFFF;
    classDef proc fill:#E6F4F6,stroke:#1B9AAA,stroke-width:1.5px,color:#123B40;
    classDef decision fill:#FBF3D9,stroke:#C9A227,stroke-width:2px,color:#5A4A00;
    classDef warn fill:#FBE9E7,stroke:#C1666B,stroke-width:1.5px,color:#6E2B26;
    classDef metric fill:#1B9AAA,stroke:#146B76,stroke-width:2px,color:#FFFFFF;
```
Read it as: a claim is never just text — it carries where it looked and
how sure it is, and the system's headline is how many claims *survive
checking*. In this demo the verification table is scripted, so the rate
illustrates the method (labelled ILLUSTRATIVE in the notebook).

## 02 · Conversation Is a Coordination Primitive — transcript as state
```mermaid
flowchart LR
    A["Analyst<br/>asks"]:::proc --> T[("Transcript<br/>the system of record")]:::metric
    T --> E["Executor<br/>answers from data"]:::proc
    E --> T
    T --> F["Findings<br/>incl. unasked-for"]:::proc
    T --> R["Replay + audit<br/>from the transcript alone"]:::io
    classDef io fill:#1A1A2E,stroke:#C9A227,stroke-width:2px,color:#FFFFFF;
    classDef proc fill:#E6F4F6,stroke:#1B9AAA,stroke-width:1.5px,color:#123B40;
    classDef metric fill:#1B9AAA,stroke:#146B76,stroke-width:2px,color:#FFFFFF;
```
Read it as: there is no side channel and no shared memory — if it is
not in the transcript, it did not happen. Audit and replay are free
because the conversation *is* the state.

## 03 · RODS — contract before capability
```mermaid
flowchart LR
    A["Write the contract<br/>Role - Output - Do-Nots - Signal"]:::proc --> L{"Linter"}:::decision
    L -->|flags| A
    L -->|CLEAN| R["Agent runs<br/>extraction"]:::proc
    R --> S["Typed signal<br/>EXTRACTION COMPLETE"]:::metric
    S --> X["Termination check<br/>ends on the signal,<br/>never on a prose word"]:::io
    classDef io fill:#1A1A2E,stroke:#C9A227,stroke-width:2px,color:#FFFFFF;
    classDef proc fill:#E6F4F6,stroke:#1B9AAA,stroke-width:1.5px,color:#123B40;
    classDef decision fill:#FBF3D9,stroke:#C9A227,stroke-width:2px,color:#5A4A00;
    classDef metric fill:#1B9AAA,stroke:#146B76,stroke-width:2px,color:#FFFFFF;
```
Read it as: four lines, checked mechanically *before* the agent runs.
A contract that fails lint never executes; a run ends on a typed
signal, not on a word an agent might say by accident.
