# Continuation

### Scheduling Tasks

Use `task-sched` to schedule persistent systemd tasks. For help, run `uvx git+https://github.com/dzackgarza/task-sched --help`.

```bash
# Add a recurring task
uvx git+https://github.com/dzackgarza/task-sched add --command "echo 'heartbeat'" --schedule "hourly"

# List scheduled tasks
uvx git+https://github.com/dzackgarza/task-sched list
```

For one-off tasks, use `at`:

```bash
echo "uvx --from git+https://github.com/dzackgarza/opencode-manager.git ocm chat ses_xxx 'continue work'" | at now + 30 minutes
```

### Waking Your Own Session

After responding to a user, your actions halt immediately until you receive a new prompt. This halts continuous or long-term work — you cannot make progress on a task that requires multiple steps if no new message arrives.

**To resume work later**, use the `at` scheduler to wake your own session:

```bash
# Get current session ID via introspection tool, then schedule a chat message:
echo "uvx --from git+https://github.com/dzackgarza/opencode-manager.git ocm chat ses_XXXXXXXX 'continue the task'" | at now + 1 minute
```

This sends a new prompt to your session at a fixed time, effectively waking you up to continue work.

**When to use:**

- Multi-step tasks where you need to pause and resume later
- Waiting for external processes or scheduled events
- Long-running work that should continue after a delay
