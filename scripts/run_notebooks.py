"""Execute every notebook in order and fail if any cell errors.

Run from the project root:
    python scripts/run_notebooks.py

Uses jupyter nbconvert, which must be installed. Each notebook is
executed in place, so its outputs and charts are saved with it.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NB = ROOT / "notebooks"
ORDER = [
    "00_setup_and_data_check.ipynb",
    "01_market_history.ipynb",
    "02_volatility_and_drawdowns.ipynb",
    "03_portfolio_risk_metrics.ipynb",
    "04_svb_case_study.ipynb",
    "05_recovery_score_and_era_comparison.ipynb",
]


def main():
    for name in ORDER:
        path = NB / name
        print("Executing", name)
        subprocess.run(
            [
                sys.executable,
                "-m",
                "jupyter",
                "nbconvert",
                "--to",
                "notebook",
                "--execute",
                str(path),
                "--output",
                name,
                "--allow-errors",
                "--ExecutePreprocessor.timeout=240",
            ],
            check=True,
            cwd=str(NB),
        )
        nb = json.loads(path.read_text())
        errors = []
        for i, cell in enumerate(nb["cells"]):
            for out in cell.get("outputs", []):
                if out.get("output_type") == "error":
                    errors.append((i, out.get("ename"), out.get("evalue")))
        if errors:
            print("ERRORS in", name, errors)
            sys.exit(1)
        print("OK, zero cell errors:", name)
    print("All notebooks executed with zero cell errors.")


if __name__ == "__main__":
    main()
