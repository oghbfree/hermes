#!/usr/bin/env python3
"""gbrain helper for Hermes — remember / recall / forget / status.
Wraps the gbrain CLI (keyless keyword-only brain at ~/.bun/bin/gbrain.exe).
Usage:
  gbrain_helper.py remember  "<fact>" [--entity <name>] [--provenance <label>]
  gbrain_helper.py recall    "<query>"
  gbrain_helper.py status
  gbrain_helper.py test
Runs gbrain with the correct env (BUN_INSTALL + PATH) since Hermes shells don't have bun on PATH.
"""
import os, sys, subprocess, shutil

BUN_BIN = os.path.join(os.path.expanduser('~'), '.bun', 'bin')
GBRAIN = os.path.join(BUN_BIN, 'gbrain.exe')
if not os.path.exists(GBRAIN):
    print(f"ERROR: gbrain not found at {GBRAIN}. Install: see hermes-configuration skill (gbrain section).", file=sys.stderr)
    sys.exit(1)

ENV = dict(os.environ)
ENV['BUN_INSTALL'] = os.path.join(os.path.expanduser('~'), '.bun')
ENV['PATH'] = BUN_BIN + os.pathsep + ENV.get('PATH', '')
GENV = 'C:\\Users\\User\\.bun'  # native win path for bun runtime


def run(args):
    cmd = [GBRAIN] + args
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, env=ENV, timeout=120, cwd=os.path.expanduser('~'))
    except Exception as e:
        print(f"ERROR running gbrain: {e}", file=sys.stderr)
        return 2
    out = (r.stdout or '') + ('\n' + r.stderr if r.stderr else '')
    # strip the [AGENT] instruction block (not user-relevant)
    if '\n[AGENT]' in out:
        out = out[:out.find('\n[AGENT]')]
    print(out.strip())
    return r.returncode


def main():
    if len(sys.argv) < 2:
        print(__doc__); return 0
    action = sys.argv[1].lower()
    if action == 'remember':
        if len(sys.argv) < 3:
            print(__doc__); return 2
        fact = sys.argv[2]
        a = ['remember', fact]
        if '--entity' in sys.argv:
            a += ['--entity', sys.argv[sys.argv.index('--entity')+1]]
        if '--provenance' in sys.argv:
            a += ['--provenance', sys.argv[sys.argv.index('--provenance')+1]]
        return run(a)
    elif action == 'recall':
        q = sys.argv[2] if len(sys.argv) > 2 else ''
        return run(['recall', '--query', q])
    elif action == 'search':
        q = sys.argv[2] if len(sys.argv) > 2 else ''
        return run(['search', q])
    elif action == 'forget':
        # forget by id
        return run(['forget', sys.argv[2]] if len(sys.argv) > 2 else __doc__)
    elif action == 'status':
        # list all facts
        return run(['recall', '--query', ''])
    elif action == 'test':
        r = run(['recall', '--query', 'gbrain'])
        return r
    else:
        print(__doc__); return 0


if __name__ == '__main__':
    sys.exit(main())