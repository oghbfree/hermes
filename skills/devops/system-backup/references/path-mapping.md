# Path Mapping Reference — execute_code vs terminal

## The Rule

| Tool | Environment | Path Format | Example |
|---|---|---|---|
| `execute_code` | Python sandbox (Windows venv) | Native Windows | `C:/Users/User/.hermes/config.yaml` |
| `terminal` | MSYS2/git-bash | POSIX-style | `/c/Users/User/.hermes/config.yaml` |

## Proof (verified 2026-05-27)

```python
# Inside execute_code Python sandbox:
os.path.exists('/c/Users/User/.hermes/config.yaml')   # FALSE
os.path.exists('C:/Users/User/.hermes/config.yaml')  # TRUE
```

```bash
# Inside terminal (MSYS bash):
ls /c/Users/User/.hermes/config.yaml    # Works
ls C:/Users/User/.hermes/config.yaml   # Fails
```

## Backup Strategy Implications

When running backup scripts:
- Use `execute_code` for Python backup scripts with **native Windows paths**
- Use `terminal` for quick file inspection with **POSIX paths**
- Never mix path styles within the same call

## Windows Sandbox Details

The `execute_code` sandbox runs:
`C:\Users\User\AppData\Local\hermes\hermes-agent\.venv\Scripts\python.exe`

With working directory `C:\c\Users\User` (MSYS-emulated).
