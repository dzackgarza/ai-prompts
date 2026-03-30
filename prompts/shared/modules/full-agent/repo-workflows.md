# Repo Workflows

## Delegating to Jules

For smaller, well-scoped issues with clear acceptance criteria — especially those that are easily verifiable (bug fixes, test additions, lint fixes, documentation) — consider delegating to Jules via GitHub issues.

**When appropriate:** straightforward tasks where the desired solution is already known, purely internal code changes, or work where research has already been done.

**When to avoid:** tasks requiring external API research, complex integration with unfamiliar libraries, or work likely to need repeated prompting.

Load the `jules` skill for the full workflow (create, monitor, review, feedback loop).

## Issues

Most tools in this environment are sourced from repos on the `dzackgarza` Github account.
If you run into failures or unexpected surprises, stop and ask the user if you should file an issue on the repo.
Do not file "bugs" for errors that have never actually been observed.
For nontrivial features: work in a worktree with a branch → PR → `@codex review` → wait 3–5 min → **LOAD `git-guidelines` skill** to scan all comment surfaces correctly.

## PRs

### Handling Review Feedback

**Reviewer comments require explicit action, not acknowledgment:**

- Never simply "acknowledge" a comment without code changes
- Every issue requires an explicit fix in an explicit commit
- If an issue is too large for the current PR (sweeping changes, touches many files), create a new PR specifically for that fix
- Never dismiss issues as "irrelevant", "out-of-scope", "won't-fix", or "acknowledged" without action
- Never pretend a PR is ready until all feedback has been explicitly addressed with code changes or new issues warranting new PRs

### What Qualifies as a PR

**PRs are for significant work only.** Do not use PRs for:

- Simple doc changes
- Trivial bugs or features easily implemented in 5-10 writes/edits
- One-off fixes that don't warrant review overhead

**PRs are appropriate for:**

- Entire features (dozens or hundreds of LOC changes)
- 10+ commits of substantive work
- Sensitive changes that might introduce regressions

PRs trigger rate-limited reviews — reserve them for changes where mistakes, regressions, or LLM failure modes are more likely.
