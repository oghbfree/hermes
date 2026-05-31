# HyperFrames — Windows Gotchas

## Path Handling (MSYS/Git Bash)

Hermes runs on Windows via git-bash (MSYS). Path translation issues are common:

| Problem | Symptom | Fix |
|---------|---------|-----|
| `cd C:\Users\User` | `No such file or directory` | Use `/c/Users/User` or `$HOME` |
| `npx hyperframes init` in wrong dir | Files land in unexpected location | Always `cd` with POSIX paths first |
| `MEDIA:/c/...` in Telegram | "Media file not found" | Use Windows-style `MEDIA:C:\Users\...` |
| `find ~/.hermes/skills` | Works fine in MSYS | No change needed |

## Render Notes

- `chrome-headless-shell` may not auto-install on Windows. If render falls back to screenshot mode, set `PRODUCER_FORCE_SCREENSHOT=true` as escape hatch.
- GPU acceleration (WebGL probe) works on most Windows machines — the renderer auto-detects. No action needed unless you see software-render fallback in logs.
- Render output path: use relative `--output final.mp4` from inside the project dir. Absolute Windows paths work but POSIX paths like `/c/...` can confuse the CLI.

## Lint Warnings (Non-Blocking)

- `composition_self_attribute_selector` — warns when a sub-composition's CSS selector matches its own `data-composition-id`. Harmless for single-use compositions; ignore unless embedding the same block multiple times.
