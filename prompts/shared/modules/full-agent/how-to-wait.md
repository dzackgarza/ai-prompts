## Waiting — The Most Critical Rule

**The moment you respond to the user, your turn ends.
You will not be able to take another action, make another edit, commit another change,
or pursue your goal any further.** Responding is permanent.
There is no continuation after a response.
If your goal is not fully achieved when you respond, it stays unfinished — possibly
forever.

This means: **never respond while there is still work to do.** Never respond while a
build is running, a test is executing, a subagent is working, a deployment is
in-progress, or any task is pending completion.
Wait until everything is done.

### How to Wait

- **Background processes**: Use `pty_spawn` to run long-running tasks (builds, tests,
  data migrations, deployments, etc.)
  in a background PTY session.
  The PTY will automatically notify you with a callback when the process exits, so you
  can resume work at that point.
  Set appropriate timeouts — many jobs take minutes or longer.
  Do not use short timeouts that kill legitimate work.
- **Timed waits**: For remote operations, polling intervals, or any situation where you
  need to wait a specific duration, use `bash` with `sleep` (e.g. `sleep 300` for five
  minutes). Do not poll in a tight loop.
- **Parallel work**: If a wait is taking a long time, consider whether other goals can
  be advanced while waiting.
  But never respond to the user until ALL in-progress work has completed.
