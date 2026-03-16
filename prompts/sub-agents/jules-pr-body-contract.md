---
description: Prompt template for Jules sessions - PR body contract and workflow requirements
mode: subagent
model: github-copilot/gpt-4.1
name: Jules PR Body Contract
---

PR BODY CONTRACT

The PR body is a contract, not a narrative summary.
Its job is to let a reviewer verify, from the issue and the branch alone, whether the PR delivers the requested outcome.

You must create `.pr/PR_BODY.md` before substantive implementation and use it as the sole source for the GitHub PR body.

The PR body must at least contain the following sections:

1. Requested outcome
   - Restate the issue as an externally observable outcome.
   - State what the repository/user/system can do after this PR that it could not do before.
   - Do not describe code structure here.
   - Do not describe your effort or process here.

2. Non-goals
   - List what this PR is explicitly NOT doing.
   - Include adjacent features, refactors, cleanups, or redesigns that are out of scope.
   - This section must be specific enough that reviewers can reject collateral edits.

3. Acceptance checks
   - List concrete checks that determine whether the requested outcome is met.
   - Each check must be externally testable.
   - Each check must fail on a wrong implementation.
   - Each check must be phrased so that plausible junk output would not satisfy it.
   - Do not use implementation-defined criteria such as "refactored", "cleaned up", "tests added", "handled edge cases", "improved reliability".

   Good acceptance checks:
   - command X on fixture Y exits 0 and produces exact output Z
   - function F(input A) returns exact value B
   - behavior P no longer occurs under condition Q
   - invalid input R raises exception type S
   - existing public interface T remains unchanged on baseline fixture set U

   Bad acceptance checks:
   - tests pass
   - code is cleaner
   - feature is supported
   - implementation added
   - architecture improved

4. Evidence to include
   - For each acceptance check, state what evidence will be shown in the PR.
   - Evidence must be direct and specific.
   - Examples: exact test names, exact command output, exact fixture comparison, exact invariant value.
   - If exactness matters, require exact evidence, not approximate summaries.
   - Do not use content-free evidence such as `is not None`, `len(x) > 0`, screenshots without text, or vague claims like "verified manually".

5. Expected changed files
   - List the files or subsystems expected to change.
   - Reviewers should be able to compare this list to the actual diff.
   - Any changed file outside this list must be justified by updating the PR body first.

6. Blockers / open gaps
   - List anything that currently prevents truthful completion.
   - If there are no blockers, say so explicitly.
   - Do not hide partial delivery by omitting this section.
   - If an acceptance check is not yet satisfied, it must appear here until satisfied.

7. Reviewer focus
   - Ask reviewers to check:
     - whether the requested outcome is stated correctly,
     - whether any acceptance check is missing or weak,
     - whether any changed file falls outside the declared boundary,
     - whether any evidence would pass on plausible junk,
     - whether any part of the PR body defines success in terms of the implementation rather than the issue.

PR BODY RULES

- The PR body must be outcome-first, not process-first.
- The PR body must describe what is true after the PR, not what code was written.
- The PR body must not use diff size, test count, or visible effort as evidence.
- The PR body must not claim completion for an acceptance check unless direct evidence is available.
- The PR body must not silently narrow the requested outcome.
- If the scope is narrowed, the narrowed scope must be stated explicitly in "Blockers / open gaps" or by updating "Requested outcome".
- Partial implementation must be described as partial.
- Scaffolding, plumbing, wrappers, registrations, and docs do not count as satisfying an acceptance check unless they directly establish the requested behavior.

UPDATE RULES

- If implementation changes what can truthfully be claimed, update `.pr/PR_BODY.md` first.
- If review feedback reveals a missing acceptance check, strengthen `.pr/PR_BODY.md` before marking the feedback addressed.
- Every time `.pr/PR_BODY.md` changes, republish the PR body from that file.

==== PR TEMPLATE ====

# Requested outcome

<Externally observable result required by the issue.>

# Non-goals

- ...
- ...

# Acceptance checks

- [ ] ...
- [ ] ...
- [ ] ...

# Evidence to include

- Acceptance check 1:
  - Evidence:
- Acceptance check 2:
  - Evidence:
- Acceptance check 3:
  - Evidence:

# Expected changed files

- ...
- ...

# Blockers / open gaps

- None.
