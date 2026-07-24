from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("wheel", type=Path)
    args = parser.parse_args()
    if not args.wheel.is_file():
        raise SystemExit(f"wheel not found: {args.wheel}")
    with tempfile.TemporaryDirectory() as directory:
        venv = Path(directory) / "venv"
        subprocess.run([sys.executable, "-m", "venv", str(venv)], check=True)
        python = venv / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
        subprocess.run(
            [str(python), "-m", "pip", "install", "--no-deps", str(args.wheel)],
            check=True,
        )
        subprocess.run(
            [
                str(python),
                "-c",
                "import agent_completion_ledger; print(agent_completion_ledger.__version__)",
            ],
            check=True,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
