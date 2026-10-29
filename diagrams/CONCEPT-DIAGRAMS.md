
# Concept Diagrams — POC Learning Lab
▸ GAI OBSERVE LLC · POC LEARNING LAB — overview materials, 2026-10-26
*One diagram per POC: the concept on one screen. Mermaid source — renders
on GitHub, stays text in the repo (versionable, no binary drift). Palette:
navy = start/deliverable · teal = process · gold = decision · strong teal =
the headline idea · rose = the flagged path. The business deck embeds these diagrams beside
their business-case patterns; the Mermaid source here is the version
of record.*

## 01 · An Agent That Sees — grounded perception + verification
```mermaid
%%{init: {"flowchart": {"nodeSpacing": 28, "rankSpacing": 44, "padding": 12}}}%%
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
%%{init: {"flowchart": {"nodeSpacing": 28, "rankSpacing": 44, "padding": 12}}}%%
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
%%{init: {"flowchart": {"nodeSpacing": 28, "rankSpacing": 44, "padding": 12}}}%%
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

## 04 · The Analyst–Executor Loop — the error is the curriculum
```mermaid
%%{init: {"flowchart": {"nodeSpacing": 28, "rankSpacing": 44, "padding": 12}}}%%
flowchart LR
    A["Question<br/>+ a data export"]:::io --> B["Analyst<br/>writes code"]:::proc
    B --> C["Executor<br/>runs it"]:::proc
    C --> D{"Typed outcome"}:::decision
    D -->|ERROR| B
    D -->|EMPTY| B
    D -->|SUCCESS| F["Finding<br/>traced to the rows"]:::metric
    classDef io fill:#1A1A2E,stroke:#C9A227,stroke-width:2px,color:#FFFFFF;
    classDef proc fill:#E6F4F6,stroke:#1B9AAA,stroke-width:1.5px,color:#123B40;
    classDef decision fill:#FBF3D9,stroke:#C9A227,stroke-width:2px,color:#5A4A00;
    classDef warn fill:#FBE9E7,stroke:#C1666B,stroke-width:1.5px,color:#6E2B26;
    classDef metric fill:#1B9AAA,stroke:#146B76,stroke-width:2px,color:#FFFFFF;
```
Read it as: the failure is not the opposite of the result — it is an
input to the next attempt. ERROR means the code was wrong, EMPTY means
the question was, and the loop treats them differently; what survives
is a finding a human can trace back to the rows it came from.

## 05 · Three Ways to Run a Group Chat — choose your parliament
```mermaid
%%{init: {"flowchart": {"nodeSpacing": 28, "rankSpacing": 44, "padding": 12}}}%%
flowchart LR
    A["Referral letter<br/>one job"]:::io --> S{"Who speaks next?"}:::decision
    S -->|fixed order| R["Round robin"]:::proc
    S -->|chosen each turn| C["Selector"]:::proc
    S -->|peer hand-off| W["Swarm"]:::proc
    R --> T[("One transcript<br/>per mode")]:::metric
    C --> T
    W --> T
    T --> P["Same pack<br/>prepared"]:::io
    classDef io fill:#1A1A2E,stroke:#C9A227,stroke-width:2px,color:#FFFFFF;
    classDef proc fill:#E6F4F6,stroke:#1B9AAA,stroke-width:1.5px,color:#123B40;
    classDef decision fill:#FBF3D9,stroke:#C9A227,stroke-width:2px,color:#5A4A00;
    classDef warn fill:#FBE9E7,stroke:#C1666B,stroke-width:1.5px,color:#6E2B26;
    classDef metric fill:#1B9AAA,stroke:#146B76,stroke-width:2px,color:#FFFFFF;
```
Read it as: the job never changes — only the parliament does. Fixed
order is predictable and spends turns; a selector pays routing calls
to stay direct; peers pull work and hand it back for verification.
Each shape leaves its own transcript, so the choice can be audited,
not just argued.

## 06 · The Debate Pattern — disagreement is a sensor
```mermaid
%%{init: {"flowchart": {"nodeSpacing": 28, "rankSpacing": 44, "padding": 12}}}%%
flowchart LR
    A["A position<br/>to be tested"]:::io --> P["Proponent<br/>strongest case FOR"]:::proc
    A --> O["Opponent<br/>strongest case AGAINST"]:::proc
    P --> J["Judge<br/>both cases + balance"]:::metric
    O --> J
    J --> H["Human review<br/>starts at the closest fight"]:::io
    classDef io fill:#1A1A2E,stroke:#C9A227,stroke-width:2px,color:#FFFFFF;
    classDef proc fill:#E6F4F6,stroke:#1B9AAA,stroke-width:1.5px,color:#123B40;
    classDef decision fill:#FBF3D9,stroke:#C9A227,stroke-width:2px,color:#5A4A00;
    classDef warn fill:#FBE9E7,stroke:#C1666B,stroke-width:1.5px,color:#6E2B26;
    classDef metric fill:#1B9AAA,stroke:#146B76,stroke-width:2px,color:#FFFFFF;
```
Read it as: the pattern decides nothing. It converts a one-sided
summary into a record of both cases and rations the scarcest resource
in governance — reviewer attention — to the argument that is hardest
to call. A real position still needs independent evidence and counsel
review.
