"""
Render all Quarto notebooks in pipeline order.

Usage:
    uv run python3 scripts/render_notebooks.py
"""
import subprocess
import sys

from cost_pred import PROJECT_ROOT

NOTEBOOKS = [
    "notebooks/00_infrastructure.qmd",
    "notebooks/rate_analysis.qmd",
    "notebooks/product_fit.qmd",
    "notebooks/market_opportunity.qmd",
]


def main() -> None:
    for nb in NOTEBOOKS:
        path = PROJECT_ROOT / nb
        print(f"\n{'='*60}")
        print(f"  Rendering {nb}")
        print(f"{'='*60}\n")

        result = subprocess.run(
            ["quarto", "render", str(path)],
            cwd=PROJECT_ROOT,
        )

        if result.returncode != 0:
            print(f"\nFailed on {nb} (exit code {result.returncode})")
            sys.exit(result.returncode)

    print(f"\n{'='*60}")
    print(f"  All notebooks rendered successfully")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
