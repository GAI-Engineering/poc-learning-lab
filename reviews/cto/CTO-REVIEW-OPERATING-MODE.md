
# CTO Review — Operating Mode (standing)
▸ GAI OBSERVE LLC · POC LEARNING LAB — public-safe process record

1. **Sessions are immutable and ID'd.** Each review session gets an
   ID (CTO-YYYY-MM-DD-<scope>-NNN) and its own file in reviews/cto/.
   A verdict, once filed, is never edited; a later session supersedes
   it by reference.
2. **The record is complete or it is not a record.** Every session
   states: the exact basis (commit/tree reviewed), the decision, the
   findings, owners and due dates for every condition, the acceptance
   evidence that will close each condition, and the change commit
   that carries the fixes.
3. **Improvement commits link back.** Any commit that answers a
   session's condition names the session ID in its message, so the
   line from finding to fix is traceable in git alone.
4. **Two verdicts, always separated.** A release can PASS as a
   learning artefact while standing HOLD as evidence of capability
   or value. The two are never merged into one word.
5. **Findings are classified.** Every finding is labelled VERIFIED
   (checked against evidence in the session), REPORTED (taken from a
   named source, not re-checked), or INFERRED (the reviewer's
   judgement) — and the action register carries the class with the
   finding. Acceptance of a fix is by independent replay where the
   session requires it, never by the fixer's own report.
6. **Public-safe copies live here.** Internal working papers stay in
   the programme's internal exchange; what a public reader needs —
   the verdict, the conditions, the disposition — is filed in
   reviews/cto/ in the repository itself.
