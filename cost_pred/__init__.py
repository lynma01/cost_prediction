from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

from cost_pred.ingest import ingest_dental
from cost_pred.llm import get_api_key, determine_product_fit
