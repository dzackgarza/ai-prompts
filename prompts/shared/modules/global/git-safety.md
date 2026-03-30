# Git Safety

## Git Workflow

All work is in **noisy repos** with others' uncommitted changes.
Use `git add`/`git commit` for checkpoints.
**For any git operation: LOAD `git-guidelines` skill.**

## Why `git restore` and `git checkout` Are Banned

These commands silently discard changes without creating an audit trail.

**Instead of reverting state directly:**

1. Commit your current work (checkpoint)
2. `git diff` to identify the rollback point
3. Apply the reverse diff as a new commit
