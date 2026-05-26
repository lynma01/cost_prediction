"""
Capture hero screenshots from rendered Quarto notebooks for the README.

Usage:
    uv run python3 scripts/capture_screenshots.py

Requires: playwright (dev dependency), rendered HTML notebooks in notebooks/
"""
from pathlib import Path

from playwright.sync_api import sync_playwright

PROJECT_ROOT = Path(__file__).parent.parent

NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
IMAGES_DIR = PROJECT_ROOT / "images"

CAPTURES = [
    {
        "html": "rate_analysis.html",
        "section_id": "rate-spread-analysis",
        "output": "rate_spread.png",
    },
    {
        "html": "product_fit.html",
        "section_id": "classification-distribution",
        "output": "classification_dist.png",
    },
    {
        "html": "market_opportunity.html",
        "section_id": "component-breakdown",
        "output": "market_breakdown.png",
    },
]


def capture_section(page, html_path: Path, section_id: str, output_path: Path) -> None:
    page.goto(f"file://{html_path}")
    page.wait_for_load_state("networkidle")

    section = page.locator(f"section#{section_id}")
    section.scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    section.screenshot(path=str(output_path))


def main() -> None:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1200, "height": 900})

        for cap in CAPTURES:
            html_path = NOTEBOOKS_DIR / cap["html"]
            output_path = IMAGES_DIR / cap["output"]

            if not html_path.exists():
                print(f"  Skipping {cap['html']} (not rendered yet)")
                continue

            print(f"  Capturing {cap['section_id']} from {cap['html']}...")
            capture_section(page, html_path, cap["section_id"], output_path)
            print(f"    -> {output_path}")

        browser.close()

    print(f"\nDone. Images saved to {IMAGES_DIR}/")


if __name__ == "__main__":
    main()
