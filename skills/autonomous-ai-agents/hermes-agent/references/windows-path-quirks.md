# Windows Path Quirks (Git-Bash / MSYS)

## LocalEnvironment cwd warning

On Windows running Hermes via Git-Bash (MSYS), the terminal backend may warn:
```
WARNING tools.environments.local: LocalEnvironment cwd '/c/Users/User' is missing on disk; falling back to '/'
```

**Cause:** The LocalEnvironment startup checks the configured `terminal.cwd` as a literal filesystem path. MSYS paths like `/c/Users/User` resolve in bash but `os.path.exists()` (bare Python on Windows) doesn't recognize them.

**Fix:** Set `terminal.cwd:` to an absolute MSYS path in `config.yaml`:
```yaml
terminal:
  cwd: /c/Users/User
```

This prevents the startup check from failing. The fallback to `/` works but produces log noise on every agent turn.

## Path Patterns That Work

| Usage | Path Pattern | Example |
|-------|-------------|---------|
| config.yaml paths | `/c/Users/<user>/...` | `/c/Users/User/.hermes/config.yaml` |
| terminal commands | Native MSYS paths | `ls /c/Users/User/` |
| read_file/search_files | Same as above | `/c/Users/User/.hermes/logs/agent.log` |
| Cron scripts (workdir) | Same | `/c/Users/User/projects/my-repo` |
